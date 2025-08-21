'use client'
import { useEffect, useState } from 'react'
import { getNextReviews, submitFeedback } from '@/lib/api'
import { Check, Clock } from 'lucide-react'
import { GlassCard } from '@/components/GlassCard'

type ReviewItem = { id: string; prompt: string; answer: string; dueInMinutes: number; ef: number; interval: number }

export default function ReviewQueue() {
  const [items, setItems] = useState<ReviewItem[]>([])
  const [reveal, setReveal] = useState<string | null>(null)

  const refresh = async () => { setItems(await getNextReviews(8)) }
  useEffect(() => { refresh() }, [])

  const rate = async (id: string, q: number) => { await submitFeedback(id, q); setItems(prev => prev.filter(x => x.id !== id)) }

  return (
    <div className="grid gap-4 md:grid-cols-2">
      {items.map((it) => (
        <GlassCard key={it.id}>
          <div className="flex items-center justify-between mb-2">
            <div className="text-xs text-gray-500 flex items-center gap-1"><Clock className="h-4 w-4 text-brand-600"/> DUE ~{it.dueInMinutes}분</div>
            <div className="text-xs text-gray-400">EF {it.ef.toFixed(2)} | {it.interval}d</div>
          </div>
          <div className="font-medium mb-2">{it.prompt}</div>
          {reveal === it.id ? (
            <div className="rounded-lg border border-brand-200 bg-white/60 p-3 text-sm text-gray-700 mb-3">{it.answer}</div>
          ) : (
            <button onClick={() => setReveal(it.id)} className="text-brand-700 text-sm underline">정답 보기</button>
          )}
          <div className="mt-3 flex gap-2">
            {[0,1,2,3,4,5].map(q => (
              <button key={q} onClick={()=>rate(it.id, q)} className="rounded-lg border bg-white/70 px-3 py-2 text-sm hover:border-brand-300 hover:shadow-glass">{q}</button>
            ))}
            <span className="ml-auto text-xs text-gray-500 flex items-center gap-1"><Check className="h-4 w-4 text-brand-600"/>기록</span>
          </div>
        </GlassCard>
      ))}
    </div>
  )
}
