from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import re

from memory import add_message, get_history
from career_agent import generate_response
from prompts import SYSTEM_PROMPT
from profiles import get_profile


app = FastAPI(
    title="AI Career Mentor",
    description="AI-powered career guidance assistant",
    version="1.0.0"
)

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------
# Request Model
# -----------------------------
class ChatRequest(BaseModel):
    session_id: str
    message: str


# -----------------------------
# Profile Extraction
# -----------------------------
def update_profile(session_id, message):

    profile = get_profile(session_id)

    text = message.lower()

    # Name
    match = re.search(
        r"my name is\s+([a-zA-Z ]+)",
        text
    )

    if match:
        profile["name"] = match.group(1).title()

    # Education
    education_keywords = [
        "b.tech",
        "btech",
        "cse",
        "computer science",
        "engineering",
        "college",
        "12th",
        "11th",
        "10th"
    ]

    for keyword in education_keywords:
        if keyword in text:
            profile["education"] = message

    # Interests
    interest_keywords = [
        "coding",
        "programming",
        "ai",
        "machine learning",
        "mathematics",
        "math",
        "physics",
        "football",
        "cricket",
        "robotics",
        "data science",
        "cybersecurity"
    ]

    for keyword in interest_keywords:
        if keyword in text:
            if keyword not in profile["interests"]:
                profile["interests"].append(keyword)


# -----------------------------
# Root
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "success",
        "message": "AI Career Mentor Backend Running"
    }


# -----------------------------
# Chat Endpoint
# -----------------------------
@app.post("/chat")
def chat(req: ChatRequest):

    # Update profile
    update_profile(
        req.session_id,
        req.message
    )

    # Save user message
    add_message(
        req.session_id,
        "user",
        req.message
    )

    # Get conversation history
    history = get_history(req.session_id)

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        }
    ]

    messages.extend(history)

    # Generate response
    reply = generate_response(messages)

    # Save AI reply
    add_message(
        req.session_id,
        "assistant",
        reply
    )

    return {
        "reply": reply,
        "session_id": req.session_id
    }


# -----------------------------
# Chat History
# -----------------------------
@app.get("/history/{session_id}")
def history(session_id):

    return {
        "session_id": session_id,
        "messages": get_history(session_id)
    }


# -----------------------------
# Student Profile
# -----------------------------
@app.get("/profile/{session_id}")
def profile(session_id):

    return get_profile(session_id)


# -----------------------------
# Recommendations
# -----------------------------
@app.get("/recommendations/{session_id}")
def recommendations(session_id):

    profile = get_profile(session_id)

    interests = profile["interests"]

    careers = []

    if "coding" in interests or "programming" in interests:
        careers.append({
            "title": "Software Engineer",
            "score": 89
        })

    if "ai" in interests or "machine learning" in interests:
        careers.append({
            "title": "AI Engineer",
            "score": 92
        })

    if (
        "mathematics" in interests
        or "math" in interests
        or "data science" in interests
    ):
        careers.append({
            "title": "Data Scientist",
            "score": 86
        })

    if "cybersecurity" in interests:
        careers.append({
            "title": "Cyber Security Engineer",
            "score": 88
        })

    if "robotics" in interests:
        careers.append({
            "title": "Robotics Engineer",
            "score": 90
        })

    scholarships = [
        "National Scholarship Portal",
        "INSPIRE Scholarship",
        "PM Scholarship Scheme"
    ]

    return {
        "careers": careers,
        "scholarships": scholarships
    }