import { NextResponse } from 'next/server'
import { readPrompt, callOpenAI } from '@/lib/openai'
import type { Direction } from '@/types'

interface Layer2Request {
  direction: Direction
  deeper?: boolean
}

export async function POST(req: Request) {
  try {
    const { direction, deeper = false, model }: Layer2Request & { model?: string } = await req.json()
    console.log(`[layer2] model: ${model}`)
    const systemPrompt = [
      readPrompt('00_SYSTEM_PRINCIPLES.md'),
      readPrompt('03_VALUE_CHAIN_DECOMPOSITION.md'),
      readPrompt('04_CHOKEPOINT_SCORING.md'),
    ].join('\n\n---\n\n')

    const userMessage = `主题：${direction.name}
背景：${direction.logic}
${deeper ? '\n用户已看过第一轮，请挖掘更深一层、更细分的上游卡脖子环节。\n' : ''}
请按完整 Serenity 流程执行：
1. 用 03_VALUE_CHAIN_DECOMPOSITION 分解该主题的完整价值链
2. 用 04_CHOKEPOINT_SCORING 对每个环节按 7 维度打分（0-100）
3. 只保留 recommended_action = continue 的环节（得分 ≥ 70），按分数降序排列
4. 输出 4-5 个卡脖子最强的上游细分方向，附上 chokepointScore

每个方向：
- name：细分方向名（10字以内）
- logic：为什么得分高，具体卡在哪里（供给约束/资质门槛/切换成本）
- exampleCompany：代表公司股票代码
- misunderstanding：投资者对这个细分的常见误区
- chokepointScore：该细分的卡脖子综合得分（0-100 整数）

只返回 JSON：
{
  "directions": [
    {
      "id": "d1",
      "name": "...",
      "logic": "...",
      "exampleCompany": "...",
      "misunderstanding": "...",
      "chokepointScore": 85
    }
  ]
}`

    const data = await callOpenAI(systemPrompt, userMessage, model)
    return NextResponse.json(data)
  } catch (err) {
    console.error('[layer2]', err)
    return NextResponse.json({ error: '调用失败' }, { status: 500 })
  }
}
