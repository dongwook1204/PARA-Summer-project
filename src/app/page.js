'use client'

import { motion } from 'framer-motion'
import TopNav from '@/components/TopNav'
import { GlassCard } from '@/components/GlassCard'
import SubjectForm from '@/components/SubjectForm'
import Link from 'next/link'

export default function Page() {
  return (
    <div className="min-h-screen">
      <TopNav />
      <main className="flex min-h-[calc(100vh-72px)] items-center justify-center px-6 py-10">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="w-full max-w-2xl">
          <GlassCard>
            <h1 className="text-3xl md:text-4xl font-semibold text-gray-900">지금 복습을 시작해보세요.</h1>
            <p className="mt-2 text-gray-600">주제를 넣으면, 그에 맞는 다양한 퀴즈를 만나보실수 있습니다.</p>
            <div className="mt-4"><SubjectForm /></div>
            <div className="mt-5 flex gap-3">
              <Link href="/dashboard" className="rounded-xl border border-brand-200 bg-white/70 px-5 py-3 text-sm hover:shadow-glass">대시보드</Link>
              <a href="#how" className="rounded-xl bg-brand-600 px-5 py-3 text-sm text-white shadow-lg shadow-brand-600/20 hover:bg-brand-700">작동 원리</a>
            </div>
          </GlassCard>

          <section id="how" className="mt-8 grid gap-4 md:grid-cols-3">
            {["SM-2", "임베딩", "알림"].map((t, i) => (
              <motion.div key={t} initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.1 * i }}>
                <GlassCard>
                  <div className="font-medium text-gray-900">{t}</div>
                  <p className="text-sm text-gray-600">개인화 주기·콘텐츠 추천·리마인더</p>
                </GlassCard>
              </motion.div>
            ))}
          </section>
        </motion.div>
      </main>
    </div>
  )
}
