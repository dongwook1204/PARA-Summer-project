from __future__ import annotations
import uuid
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from threading import Lock
from typing import Dict, List
from .sm2 import SM2State, update_sm2

@dataclass
class Card:
    id: str
    subject: str
    prompt: str
    answer: str
    state: SM2State = field(default_factory=SM2State)
    due_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

class MemoryStore:
    def __init__(self) -> None:
        self.cards: Dict[str, Card] = {}
        self.subject_index: Dict[str, List[str]] = {}
        self.lock = Lock()

    def add_cards(self, subject: str, pairs: List[tuple[str, str]]):
        with self.lock:
            for prompt, answer in pairs:
                cid = str(uuid.uuid4())
                card = Card(id=cid, subject=subject, prompt=prompt, answer=answer)
                self.cards[cid] = card
                self.subject_index.setdefault(subject, []).append(cid)

    def get_due(self, limit: int = 10) -> List[Card]:
        with self.lock:
            now = datetime.now(timezone.utc)
            due = sorted(self.cards.values(), key=lambda c: c.due_at)
            return [c for c in due if c.due_at <= now][:limit]

    def update_feedback(self, card_id: str, quality: int) -> Card | None:
        with self.lock:
            card = self.cards.get(card_id)
            if not card:
                return None
            card.state = update_sm2(card.state, quality)
            card.due_at = datetime.now(timezone.utc) + timedelta(days=card.state.interval)
            return card

    def search(self, q: str) -> List[Card]:
        ql = q.lower()
        with self.lock:
            return [
                c for c in self.cards.values()
                if ql in c.prompt.lower() or ql in c.answer.lower() or ql in c.subject.lower()
            ]

STORE = MemoryStore()
