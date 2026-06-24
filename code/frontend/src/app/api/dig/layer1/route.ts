import { NextResponse } from 'next/server'
import { readPrompt, callOpenAI } from '@/lib/openai'

export async function POST(req: Request) {
  try {
    const body = await req.json().catch(() => ({}))
    const model: string = body.model
    console.log(`[layer1] model: ${model}`)
    const systemPrompt = [
      readPrompt('00_SYSTEM_PRINCIPLES.md'),
      readPrompt('02_THEME_RESEARCH.md'),
    ].join('\n\n---\n\n')

    const userMessage = `按照 Serenity 方法论完整评估后，识别 4-5 个当前值得深挖上游的结构性主题。

要求：
- 先经过 02_THEME_RESEARCH 的结构性验证（趋势真实性、持续性、下游支出来源）
- 只保留 continue_to_value_chain = true 的主题
- 每个主题代表一个中下游需求方向，上游供给端尚未充分定价
- name：主题名（10字以内，中文）
- logic：这个主题为何产生上游卡脖子压力（结合 02 的分析框架，2-3句话）
- exampleCompany：一个上游代表公司股票代码
- misunderstanding：大多数投资者对这个主题的典型误判

只返回 JSON：
{
  "directions": [
    { "id": "d1", "name": "...", "logic": "...", "exampleCompany": "...", "misunderstanding": "..." }
  ]
}`

    const data = await callOpenAI(systemPrompt, userMessage, model)
    return NextResponse.json(data)
  } catch (err) {
    console.error('[layer1]', err)
    return NextResponse.json({ error: '调用失败' }, { status: 500 })
  }
}
