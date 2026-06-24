'use client'

import { motion } from 'motion/react'
import type { Direction } from '@/types'

interface Props {
  direction: Direction
  index: number
  onSelect: (direction: Direction) => void
  disabled?: boolean
}

function ChokepointBar({ score }: { score: number }) {
  const color =
    score >= 85 ? 'bg-emerald-500' :
    score >= 70 ? 'bg-primary' :
    'bg-amber-500'

  return (
    <div className="flex items-center gap-2">
      <div className="flex-1 h-1 bg-border rounded-full overflow-hidden">
        <div className={`h-full rounded-full transition-all ${color}`} style={{ width: `${score}%` }} />
      </div>
      <span className="text-xs font-mono text-muted-foreground tabular-nums">{score}</span>
    </div>
  )
}

export function DirectionCard({ direction, index, onSelect, disabled }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 16 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08, duration: 0.3 }}
    >
      <button
        onClick={() => onSelect(direction)}
        disabled={disabled}
        className="w-full text-left rounded-xl border border-border bg-card p-5 space-y-3
          hover:border-primary/60 hover:bg-card/80 transition-all duration-200
          disabled:opacity-50 disabled:cursor-not-allowed
          focus:outline-none focus:ring-2 focus:ring-primary/40 group"
      >
        <div className="flex items-start justify-between gap-3">
          <h3 className="font-semibold text-foreground text-base leading-snug group-hover:text-primary transition-colors">
            {direction.name}
          </h3>
          <span className="shrink-0 text-muted-foreground text-sm mt-0.5 group-hover:text-primary transition-colors">→</span>
        </div>

        <p className="text-sm text-muted-foreground leading-relaxed">
          {direction.logic}
        </p>

        {direction.chokepointScore !== undefined && (
          <div className="space-y-1">
            <p className="text-xs text-muted-foreground">卡脖子得分</p>
            <ChokepointBar score={direction.chokepointScore} />
          </div>
        )}

        {direction.exampleCompany && (
          <p className="text-xs text-muted-foreground/70">
            代表公司：{direction.exampleCompany}
          </p>
        )}

        <div className="border-t border-border pt-3">
          <p className="text-xs text-primary/80">
            市场误解：{direction.misunderstanding}
          </p>
        </div>
      </button>
    </motion.div>
  )
}
