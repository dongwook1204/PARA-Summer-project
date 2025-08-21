from __future__ import annotations
from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .store import STORE
from .ai import generate_cards

app = FastAPI(title="ReloadK API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SubjectReq(BaseModel):
    subject: str

class FeedbackReq(BaseModel):
    quality: int  # 0~5

class ReviewItem(BaseModel):
    id: str
    prompt: str
    answer: str
    dueInMinutes: int
    ef: float
    interval: int

class ContentItem(BaseModel):
    id: str
    title: str
    tags: list[str]
    snippet: str

@app.post("/subjects")
def create_subject(req: SubjectReq):
    subject = req.subject.strip()
    if not subject:
        raise HTTPException(400, "subject required")
    pairs = generate_cards(subject)
    STORE.add_cards(subject, pairs)
    return {"subject": subject, "count": len(pairs), "status": "ready"}

@app.get("/reviews/next", response_model=list[ReviewItem])
def get_next(limit: int = 10):
    cards = STORE.get_due(limit=limit)
    now = datetime.now(timezone.utc)
    items: list[ReviewItem] = []
    for c in cards:
        due_min = max(0, int((c.due_at - now).total_seconds() // 60))
        items.append(ReviewItem(
            id=c.id,
            prompt=c.prompt,
            answer=c.answer,
            dueInMinutes=due_min,
            ef=c.state.ef,
            interval=c.state.interval,
        ))
    return items

@app.post("/reviews/{card_id}/feedback")
def feedback(card_id: str, req: FeedbackReq):
    updated = STORE.update_feedback(card_id, req.quality)
    if not updated:
        raise HTTPException(404, "card not found")
    return {"ok": True, "next_due": updated.due_at.isoformat()}

@app.get("/content/search", response_model=list[ContentItem])
def search(q: str):
    res = STORE.search(q)
    items = [ContentItem(id=c.id, title=f"{c.subject} — 카드", tags=[c.subject], snippet=c.prompt) for c in res[:20]]
    return items
