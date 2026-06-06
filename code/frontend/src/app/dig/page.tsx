'use client'

import { useEffect } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { DirectionCard } from '@/components/DirectionCard'
import { StockCard } from '@/components/StockCard'
import { useDigStore } from '@/store/useDigStore'

const LAYER_LABELS = ['', '选择中下游方向', '选择上游子方向', '挖掘结果']

function LayerIndicator({ current }: { current: number }) {
  return (
    <div className="flex items-center gap-2">
      {[1, 2, 3].map((n) => (
        <div key={n} className="flex items-center gap-2">
          <div className={`flex items-center justify-center w-7 h-7 rounded-full text-xs font-bold transition-all duration-300 ${
            n < current ? 'bg-primary text-primary-foreground' :
            n === current ? 'bg-primary/20 border border-primary text-primary' :
            'bg-muted text-muted-foreground'
          }`}>
            {n < current ? '✓' : n}
          </div>
          {n < 3 && (
            <div className={`w-8 h-px transition-colors duration-300 ${n < current ? 'bg-primary' : 'bg-border'}`} />
          )}
        </div>
      ))}
    </div>
  )
}

function LoadingSkeleton() {
  return (
    <div className="space-y-3">
      {[1, 2, 3].map((n) => (
        <div key={n} className="rounded-xl border border-border bg-card p-5 animate-pulse">
          <div className="h-4 bg-muted rounded w-1/3 mb-3" />
          <div className="h-3 bg-muted rounded w-full mb-2" />
          <div className="h-3 bg-muted rounded w-4/5" />
        </div>
      ))}
    </div>
  )
}

export default function DigPage() {
  const {
    layer, loading, error,
    layer1Directions, layer2Directions, finalStocks,
    selectedLayer1, selectedLayer2,
    startDig, selectLayer1, selectLayer2, digDeeper, reset,
  } = useDigStore()

  useEffect(() => {
    if (layer === 0) {
      startDig()
    }
  }, [])

  return (
    <main className="min-h-screen px-6 py-10">
      <div className="max-w-2xl mx-auto space-y-8">

        {/* Header */}
        <div className="flex items-center justify-between">
          <Link href="/" className="text-sm text-muted-foreground hover:text-foreground transition-colors">
            ← 返回首页
          </Link>
          <LayerIndicator current={layer || 1} />
        </div>

        {/* Breadcrumb */}
        {(selectedLayer1 || selectedLayer2) && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex items-center gap-2 text-sm text-muted-foreground flex-wrap"
          >
            {selectedLayer1 && (
              <span className="bg-primary/10 text-primary px-2.5 py-1 rounded-full text-xs">
                {selectedLayer1.name}
              </span>
            )}
            {selectedLayer2 && (
              <>
                <span>→</span>
                <span className="bg-primary/10 text-primary px-2.5 py-1 rounded-full text-xs">
                  {selectedLayer2.name}
                </span>
              </>
            )}
          </motion.div>
        )}

        {/* Title */}
        <div>
          <h2 className="text-2xl font-bold text-foreground">
            {LAYER_LABELS[layer || 1]}
          </h2>
          {layer === 1 && (
            <p className="text-muted-foreground mt-1 text-sm">点击一个方向，AI 将沿这条产业链向上游挖掘</p>
          )}
          {layer === 2 && (
            <p className="text-muted-foreground mt-1 text-sm">选择一个更细分的上游环节继续深挖</p>
          )}
          {layer === 3 && (
            <p className="text-muted-foreground mt-1 text-sm">以下是卡在关键节点、尚未被重新估值的公司</p>
          )}
        </div>

        {/* Error */}
        {error && (
          <div className="rounded-xl border border-destructive/30 bg-destructive/10 p-4 text-sm text-destructive">
            {error}
          </div>
        )}

        {/* Content */}
        <AnimatePresence mode="wait">
          {loading ? (
            <motion.div key="loading" initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>
              <LoadingSkeleton />
            </motion.div>
          ) : (
            <motion.div key={`layer-${layer}`} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}>

              {/* Layer 1 */}
              {layer === 1 && (
                <div className="space-y-3">
                  {layer1Directions.map((dir, i) => (
                    <DirectionCard
                      key={dir.id}
                      direction={dir}
                      index={i}
                      onSelect={selectLayer1}
                    />
                  ))}
                </div>
              )}

              {/* Layer 2 */}
              {layer === 2 && (
                <div className="space-y-3">
                  {layer2Directions.map((dir, i) => (
                    <DirectionCard
                      key={dir.id}
                      direction={dir}
                      index={i}
                      onSelect={selectLayer2}
                    />
                  ))}
                </div>
              )}

              {/* Layer 3 - Results */}
              {layer === 3 && (
                <div className="space-y-4">
                  <div className="space-y-3">
                    {finalStocks.map((stock, i) => (
                      <StockCard key={stock.id} stock={stock} index={i} />
                    ))}
                  </div>

                  <div className="flex gap-3 pt-4">
                    <Button
                      variant="outline"
                      onClick={digDeeper}
                      className="flex-1 cursor-pointer"
                    >
                      再挖一层
                    </Button>
                    <Button
                      variant="outline"
                      onClick={reset}
                      className="flex-1 cursor-pointer"
                    >
                      重新开始
                    </Button>
                  </div>

                  <p className="text-xs text-center text-muted-foreground pt-2">
                    内容仅供研究参考，不构成投资建议。AI 无法获取实时股价，具体数据请自行验证。
                  </p>
                </div>
              )}

            </motion.div>
          )}
        </AnimatePresence>

      </div>
    </main>
  )
}
