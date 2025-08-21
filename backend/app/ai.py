from __future__ import annotations
from typing import List, Tuple

# (기본 버전) 간단 카드 생성기 - 하드코딩/룰베이스
def generate_cards(subject: str) -> List[Tuple[str, str]]:
    return [
        (f"{subject} 핵심 개념 요약은?", f"{subject}의 핵심 정의/공식/예시를 간단히 정리."),
        (f"{subject} 기초 확인: A와 B 차이는?", "정의·성질·예시로 비교"),
        (f"{subject}에서 자주 하는 실수 2가지는?", "개념 오해 / 계산 실수"),
        (f"{subject} 핵심 3가지?", "핵심정의, 기본공식, 응용전략"),
        (f"{subject} 초급 퀴즈 1", "간단 정답"),
        (f"{subject} 초급 퀴즈 2", "간단 정답"),
    ]
