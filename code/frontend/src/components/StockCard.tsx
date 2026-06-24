'use client'

import { motion } from 'motion/react'
import type { Stock, Classification, ValuationStatus, CrowdingStatus, ExposureCategory } from '@/types'

// ── 分类标签 ──────────────────────────────────────────────
const classificationStyle: Record<Classification, string> = {
  'High Priority Research': 'bg-emerald-500/15 text-emerald-400 border-emerald-500/30',
  'Watchlist':              'bg-primary/15 text-primary border-primary/30',
  'Wait for Pullback':      'bg-amber-500/15 text-amber-400 border-amber-500/30',
  'Observe':                'bg-muted text-muted-foreground border-border',
}

const classificationLabel: Record<Classification, string> = {
  'High Priority Research': '优先研究',
  'Watchlist':              '观察名单',
  'Wait for Pullback':      '等待回调',
  'Observe':                '持续观察',
}

// ── 市场标签 ──────────────────────────────────────────────
const marketStyle: Record<string, string> = {
  'A股': 'bg-rose-500/15 text-rose-400 border-rose-500/30',
  '港股': 'bg-sky-500/15 text-sky-400 border-sky-500/30',
  '美股': 'bg-violet-500/15 text-violet-400 border-violet-500/30',
}

// ── 暴露类型 ──────────────────────────────────────────────
const exposureLabel: Record<ExposureCategory, string> = {
  pure_play:       '纯玩法',
  high_exposure:   '高暴露',
  partial_exposure:'部分暴露',
}

const exposureStyle: Record<ExposureCategory, string> = {
  pure_play:       'text-emerald-400',
  high_exposure:   'text-primary',
  partial_exposure:'text-muted-foreground',
}

// ── 估值状态 ──────────────────────────────────────────────
const valuationLabel: Record<ValuationStatus, string> = {
  undemanding:   '估值便宜',
  reasonable:    '估值合理',
  stretched:     '估值偏贵',
  very_stretched:'估值很贵',
  unknown:       '估值未知',
}

const valuationStyle: Record<ValuationStatus, string> = {
  undemanding:   'text-emerald-400',
  reasonable:    'text-primary',
  stretched:     'text-amber-400',
  very_stretched:'text-rose-400',
  unknown:       'text-muted-foreground',
}

// ── 拥挤度 ──────────────────────────────────────────────
const crowdingLabel: Record<CrowdingStatus, string> = {
  low:     '低拥挤',
  medium:  '中拥挤',
  high:    '高拥挤',
  unknown: '未知',
}

const crowdingStyle: Record<CrowdingStatus, string> = {
  low:     'text-emerald-400',
  medium:  'text-amber-400',
  high:    'text-rose-400',
  unknown: 'text-muted-foreground',
}

// ── 商业验证等级 ──────────────────────────────────────────
function ValidationDots({ level }: { level: 0 | 1 | 2 | 3 }) {
  return (
    <div className="flex items-center gap-1">
      {[1, 2, 3].map((n) => (
        <div
          key={n}
          className={`w-2 h-2 rounded-full transition-colors ${
            n <= level ? 'bg-primary' : 'bg-border'
          }`}
        />
      ))}
    </div>
  )
}

// ── 最终得分环 ──────────────────────────────────────────
function ScoreBadge({ score }: { score: number }) {
  const color = score >= 82 ? 'text-emerald-400' : score >= 65 ? 'text-primary' : 'text-amber-400'
  return (
    <div className={`font-mono font-bold text-lg ${color}`}>
      {score}<span className="text-xs font-normal text-muted-foreground">/100</span>
    </div>
  )
}

// ── 每个信息块 ──────────────────────────────────────────
function Section({
  label,
  children,
  variant = 'default',
}: {
  label: string
  children: React.ReactNode
  variant?: 'default' | 'warning' | 'primary'
}) {
  const labelClass =
    variant === 'warning' ? 'text-amber-400/80' :
    variant === 'primary' ? 'text-primary/80' :
    'text-muted-foreground'

  const textClass =
    variant === 'warning' ? 'text-amber-300/90' :
    variant === 'primary' ? 'text-primary' :
    'text-foreground'

  return (
    <div className="space-y-1">
      <p className={`text-xs uppercase tracking-wide ${labelClass}`}>{label}</p>
      <p className={`text-sm leading-relaxed ${textClass}`}>{children}</p>
    </div>
  )
}

// ── 主组件 ──────────────────────────────────────────────
interface Props {
  stock: Stock
  index: number
}

export function StockCard({ stock, index }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.1, duration: 0.35 }}
      className="rounded-xl border border-border bg-card p-5 space-y-4"
    >
      {/* 头部：公司 + 市场 + 分类 + 得分 */}
      <div className="flex items-start justify-between gap-3">
        <div className="space-y-0.5 min-w-0">
          <h3 className="font-bold text-foreground text-lg leading-snug truncate">{stock.name}</h3>
          <p className="font-mono text-primary text-sm">{stock.ticker}</p>
        </div>
        <div className="flex flex-col items-end gap-1.5 shrink-0">
          <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${marketStyle[stock.market] ?? ''}`}>
            {stock.market}
          </span>
          <span className={`text-xs font-medium px-2.5 py-1 rounded-full border ${classificationStyle[stock.classification]}`}>
            {classificationLabel[stock.classification]}
          </span>
        </div>
      </div>

      {/* 元数据行：暴露 / 验证 / 估值 / 拥挤 / 得分 */}
      <div className="flex flex-wrap items-center gap-x-4 gap-y-2 text-xs border-t border-border pt-3">
        <span className={`font-medium ${exposureStyle[stock.exposureCategory]}`}>
          {exposureLabel[stock.exposureCategory]}
        </span>

        <div className="flex items-center gap-1.5 text-muted-foreground">
          <span>验证</span>
          <ValidationDots level={stock.commercialValidationLevel} />
          <span className="text-muted-foreground/60">L{stock.commercialValidationLevel}</span>
        </div>

        <span className={valuationStyle[stock.valuationStatus]}>
          {valuationLabel[stock.valuationStatus]}
        </span>

        <span className={crowdingStyle[stock.crowdingStatus]}>
          {crowdingLabel[stock.crowdingStatus]}
        </span>

        <div className="ml-auto">
          <ScoreBadge score={stock.finalScore} />
        </div>
      </div>

      {/* 一句话论文 */}
      <div className="rounded-lg bg-primary/5 border border-primary/20 px-3 py-2">
        <p className="text-sm text-foreground/90 leading-relaxed italic">
          {stock.oneSentenceThesis}
        </p>
      </div>

      {/* 核心逻辑 / 熊市论证 / 催化剂 */}
      <div className="space-y-3 border-t border-border pt-3">
        <Section label="核心逻辑">{stock.coreLogic}</Section>
        <Section label="⚠ 熊市论证" variant="warning">{stock.bearCase}</Section>
        <Section label="催化剂" variant="primary">{stock.catalyst}</Section>
      </div>
    </motion.div>
  )
}
