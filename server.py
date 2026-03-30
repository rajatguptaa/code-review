import os
import json
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from agent import code_review_agent
from schemas import CodeReview

app = FastAPI(
    title="CodeReview Agent API",
    description="AI-powered code reviewer — submit code snippets, get structured feedback with bug detection, severity ratings, and refactored suggestions.",
)

session_service = InMemorySessionService()
runner = Runner(agent=code_review_agent, app_name="code-review-agent", session_service=session_service)


class ReviewRequest(BaseModel):
    code: str = """\ndef calculate_average(numbers):\n    total = 0\n    for i in range(len(numbers)):\n        total += numbers[i]\n    average = total / len(numbers)\n    return average\n"""


@app.post("/review", response_model=CodeReview)
async def review_code(request: ReviewRequest):
    try:
        session = await session_service.create_session(app_name="code-review-agent", user_id="user")
        content = types.Content(role="user", parts=[types.Part(text=request.code)])

        final_response = None
        async for event in runner.run_async(
            user_id="user",
            session_id=session.id,
            new_message=content
        ):
            if event.is_final_response() and event.content and event.content.parts:
                final_response = event.content.parts[0].text
                break

        if not final_response:
            raise ValueError("No response from agent")

        # Clean up markdown code blocks if the LLM wraps the JSON
        text = final_response.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
            text = text.strip()

        return CodeReview(**json.loads(text))

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent Error: {str(e)}")


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
