'use client'

import { motion } from 'motion/react'
import type { Direction } from '@/types'

interface Props {
  direction: Direction
  index: number
  onSelect: (direction: Direction) => void
  disabled?: boolean
}

export function DirectionCard({ direction, index, onSelect, disabled }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.08, duration: 0.35 }}
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
