from __future__ import annotations
from dataclasses import dataclass

@dataclass
class SM2State:
    repetitions: int = 0
    interval: int = 0  # days
    ef: float = 2.5

def update_sm2(state: SM2State, quality: int) -> SM2State:
    q = max(0, min(5, int(quality)))
    if q < 3:
        return SM2State(repetitions=0, interval=1, ef=state.ef)

    reps = state.repetitions + 1
    if reps == 1:
        interval = 1
    elif reps == 2:
        interval = 6
    else:
        interval = round(max(1, state.interval) * state.ef)

    ef = state.ef + (0.1 - (5 - q) * (0.08 + (5 - q) * 0.02))
    if ef < 1.3:
        ef = 1.3

    return SM2State(repetitions=reps, interval=interval, ef=ef)
