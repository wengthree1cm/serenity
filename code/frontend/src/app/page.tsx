import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ModelSelector } from '@/components/ModelSelector'

export default function HomePage() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center px-6">
      <div className="absolute top-5 right-6">
        <ModelSelector />
      </div>
      <div className="max-w-2xl w-full text-center space-y-10">

        <div className="space-y-4">
          <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
            基于 Cyrianity 投资方法论
          </div>
          <h1 className="text-5xl font-bold tracking-tight text-foreground">
            Investment Digger
          </h1>
          <p className="text-xl text-muted-foreground leading-relaxed">
            沿产业链向上游挖掘，定位估值错位的卡脖子公司
          </p>
        </div>

        <div className="grid grid-cols-3 gap-4 text-sm">
          {[
            { step: '01', label: '选择中下游方向', desc: 'AI 给出 3-5 个有潜力的产业方向' },
            { step: '02', label: '向上游挖掘', desc: '沿供应链追溯到关键卡脖子环节' },
            { step: '03', label: '定位潜力股', desc: '输出具体公司、代码与催化剂' },
          ].map((item) => (
            <div key={item.step} className="rounded-xl border border-border bg-card p-4 text-left space-y-2">
              <span className="text-primary font-mono font-bold text-lg">{item.step}</span>
              <p className="font-medium text-foreground">{item.label}</p>
              <p className="text-muted-foreground text-xs leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>

        <div className="space-y-3">
          <Link href="/dig">
            <Button size="lg" className="px-10 py-6 text-lg font-semibold rounded-xl cursor-pointer">
              开始挖掘
            </Button>
          </Link>
          <p className="text-xs text-muted-foreground">
            内容仅供研究参考，不构成投资建议
          </p>
        </div>

      </div>
    </main>
  )
}
