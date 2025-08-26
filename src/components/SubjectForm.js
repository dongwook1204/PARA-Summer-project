'use client'
import { useState } from 'react'
import { createSubjectPlan } from '@/lib/api'

export default function SubjectForm() {
  const [subject, setSubject] = useState('')
  const [loading, setLoading] = useState(false)
  const [ok, setOk] = useState(false)

  const onSubmit = async (e) => {
    e.preventDefault()
    if (!subject.trim()) return
    setLoading(true)
    setOk(false)
    try {
      await createSubjectPlan(subject.trim())
      setOk(true)
      setSubject('')
    } finally {
      setLoading(false)
    }
  }

  return (
    <form onSubmit={onSubmit} className="flex w-full max-w-xl flex-col gap-3">
      <input
        value={subject}
        onChange={(e)=>setSubject(e.target.value)}
        placeholder="미적분, 한국사, 토익 RC"
        className="w-full rounded-xl border border-brand-200 bg-white/70 px-4 py-3 outline-none placeholder:text-gray-400 focus:ring-4 focus:ring-brand-200"
      />
      <button
        disabled={loading}
        className="rounded-xl bg-brand-600 px-5 py-3 text-white shadow-lg shadow-brand-600/20 hover:bg-brand-700 transition disabled:opacity-60"
      >
        {loading ? '등록 중...' : '주제 등록'}
      </button>
      {ok && <div className="text-sm text-brand-700 bg-brand-100 rounded-lg px-3 py-2 border border-brand-200">등록되었습니다.</div>}
    </form>
  )
}
