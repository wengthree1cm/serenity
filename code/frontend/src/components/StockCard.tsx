'use client'

import { motion } from 'motion/react'
import { Badge } from '@/components/ui/badge'
import type { Stock } from '@/types'

interface Props {
  stock: Stock
  index: number
}

const marketColors: Record<string, string> = {
  'A股': 'bg-rose-500/15 text-rose-400 border-rose-500/30',
  '港股': 'bg-sky-500/15 text-sky-400 border-sky-500/30',
  '美股': 'bg-violet-500/15 text-violet-400 border-violet-500/30',
}

export function StockCard({ stock, index }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.35 }}
      className="rounded-xl border border-border bg-card p-5 space-y-4"
    >
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-bold text-foreground text-lg">{stock.name}</h3>
          <p className="font-mono text-primary text-sm mt-0.5">{stock.ticker}</p>
        </div>
        <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${marketColors[stock.market] ?? ''}`}>
          {stock.market}
        </span>
      </div>

      <div className="space-y-2">
        <div>
          <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">核心逻辑</p>
          <p className="text-sm text-foreground leading-relaxed">{stock.coreLogic}</p>
        </div>
        <div className="border-t border-border pt-3">
          <p className="text-xs text-muted-foreground uppercase tracking-wide mb-1">估值重构催化剂</p>
          <p className="text-sm text-primary leading-relaxed">{stock.catalyst}</p>
        </div>
      </div>
    </motion.div>
  )
}
