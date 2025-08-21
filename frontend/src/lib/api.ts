export const API_BASE = process.env.NEXT_PUBLIC_API_BASE || "http://localhost:8000";

export type ReviewItem = { id: string; prompt: string; answer: string; dueInMinutes: number; ef: number; interval: number };

export async function getNextReviews(limit = 10): Promise<ReviewItem[]> {
  const res = await fetch(`${API_BASE}/reviews/next?limit=${limit}`, { cache: 'no-store' });
  if (!res.ok) throw new Error('리뷰 대기열 조회 실패');
  return res.json();
}

export async function submitFeedback(reviewId: string, quality: number) {
  const res = await fetch(`${API_BASE}/reviews/${reviewId}/feedback`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ quality })
  });
  if (!res.ok) throw new Error('피드백 전송 실패');
  return res.json();
}

export async function createSubjectPlan(subject: string) {
  const res = await fetch(`${API_BASE}/subjects`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ subject })
  });
  if (!res.ok) throw new Error('주제 등록 실패');
  return res.json();
}
