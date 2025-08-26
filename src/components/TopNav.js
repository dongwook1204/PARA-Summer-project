import { CheckCircle2 } from 'lucide-react'

export default function TopNav() {
  return (
    <div className="w-full flex items-center justify-between px-6 py-4">
      <div className="flex items-center gap-2">
        <CheckCircle2 className="h-6 w-6 text-brand-600" />
        <span className="font-semibold text-xl">ReloadK</span>
        <span className="ml-2 text-xs text-brand-600/80 bg-brand-100 px-2 py-0.5 rounded-full">Beta</span>
      </div>
      <div className="text-sm text-gray-500">AI 복습 최적화</div>
    </div>
  )
}
