from pydantic import BaseModel, Field
from typing import List, Literal


class CodeIssue(BaseModel):
    """
    A single issue found during the code review.
    Using 'Literal' forces the model to choose from a strict list of options.
    """
    line_reference: str = Field(description="The specific line or code snippet where the issue was found.")
    severity: Literal["Critical", "Warning", "Info"] = Field(description="Severity level: Critical for bugs/security, Warning for code smells, Info for style suggestions.")
    category: Literal["Bug", "Security", "Performance", "Readability", "Best Practice"] = Field(description="Category of the issue found.")
    description: str = Field(description="Clear explanation of why this is an issue.")
    suggestion: str = Field(description="Specific fix or improvement suggestion with corrected code if applicable.")


class CodeReview(BaseModel):
    """
    This schema defines the exact structure we want the Gemini model to return.
    Forces Gemini to return a precise, actionable code review every time.
    """
    summary: str = Field(description="A 2-3 sentence overall assessment of the code quality.")
    language_detected: str = Field(description="The programming language of the submitted code (e.g., Python, JavaScript, Java).")
    issues: List[CodeIssue] = Field(description="List of all issues found in the code, ordered by severity (Critical first).")
    score: Literal["A", "B", "C", "D", "F"] = Field(description="Overall code quality grade: A=Excellent, B=Good, C=Needs Improvement, D=Poor, F=Critical Issues.")
    refactored_snippet: str = Field(description="A refactored version of the most critical section of the code, showing the recommended fix.")
