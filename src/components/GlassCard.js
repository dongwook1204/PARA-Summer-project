import { cn } from '@/components/cn'

export function GlassCard({ className, children }) {
  return (
    <div className={cn('rounded-2xl bg-white/40 backdrop-blur-xl glass-border shadow-glass border p-6', className)}>
      {children}
    </div>
  )
}
