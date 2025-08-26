'use client'
import { motion } from 'framer-motion'
import TopNav from '@/components/TopNav'
import { GlassCard } from '@/components/GlassCard'
import ReviewQueue from '@/components/ReviewQueue'

export default function DashboardPage() {
  return (
    <div className="min-h-screen">
      <TopNav />
      <main className="px-6 py-8 max-w-6xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.5 }} className="grid gap-4 md:grid-cols-3">
          <GlassCard><Stat title="오늘" value="8" /></GlassCard>
          <GlassCard><Stat title="연속" value="5" /></GlassCard>
          <GlassCard><Stat title="EF" value="2.35" /></GlassCard>
        </motion.div>

        <div className="mt-6">
          <h2 className="mb-3 text-xl font-semibold">대기열</h2>
          <ReviewQueue />
        </div>
      </main>
    </div>
  )
}

function Stat({ title, value }) {
  return (
    <div>
      <div className="text-sm text-gray-600">{title}</div>
      <div className="mt-1 text-3xl font-bold">{value}</div>
    </div>
  )
}
