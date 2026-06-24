'use client'

import { useState } from 'react'
import { MODELS } from '@/lib/models'
import { useDigStore } from '@/store/useDigStore'

const tierStyle = {
  cheap:    'text-emerald-400',
  balanced: 'text-primary',
  best:     'text-violet-400',
}

const tierLabel = {
  cheap:    '便宜',
  balanced: '均衡',
  best:     '旗舰',
}

export function ModelSelector() {
  const { model, setModel } = useDigStore()
  const [open, setOpen] = useState(false)
  const current = MODELS.find(m => m.id === model) ?? MODELS[2]

  return (
    <div className="relative">
      <button
        onClick={() => setOpen(o => !o)}
        className="flex items-center gap-2 rounded-lg border border-border bg-card px-3 py-1.5
          text-sm hover:border-primary/50 transition-colors focus:outline-none"
      >
        <span className={`text-xs font-medium ${tierStyle[current.tier]}`}>
          {tierLabel[current.tier]}
        </span>
        <span className="text-foreground font-medium">{current.label}</span>
        <span className="text-muted-foreground text-xs">▾</span>
      </button>

      {open && (
        <>
          {/* 背景遮罩 */}
          <div className="fixed inset-0 z-10" onClick={() => setOpen(false)} />

          <div className="absolute right-0 top-full mt-1 z-20 w-64 rounded-xl border border-border bg-card shadow-lg overflow-hidden">
            <div className="p-1.5 space-y-0.5">
              {MODELS.map(m => (
                <button
                  key={m.id}
                  onClick={() => { setModel(m.id); setOpen(false) }}
                  className={`w-full text-left px-3 py-2.5 rounded-lg flex items-start justify-between gap-3
                    hover:bg-muted transition-colors
                    ${m.id === model ? 'bg-primary/10' : ''}`}
                >
                  <div className="space-y-0.5 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-sm font-medium text-foreground">{m.label}</span>
                      {m.id === model && (
                        <span className="text-xs text-primary">✓</span>
                      )}
                    </div>
                    <p className="text-xs text-muted-foreground">{m.desc}</p>
                  </div>
                  <span className={`text-xs font-medium shrink-0 mt-0.5 ${tierStyle[m.tier]}`}>
                    {tierLabel[m.tier]}
                  </span>
                </button>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}
