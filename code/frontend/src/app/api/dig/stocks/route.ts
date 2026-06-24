import { NextResponse } from 'next/server'
import { readPrompt, callOpenAI } from '@/lib/openai'
import type { Direction } from '@/types'

interface StocksRequest {
  layer1: Direction
  layer2: Direction
}

export async function POST(req: Request) {
  try {
    const { layer1, layer2 }: StocksRequest = await req.json()

    const systemPrompt = [
      readPrompt('00_SYSTEM_PRINCIPLES.md'),
      readPrompt('05_COMPANY_DISCOVERY.md'),
      readPrompt('06_COMMERCIAL_VALIDATION.md'),
      readPrompt('07_FINANCIAL_VALUATION_CROWDING.md'),
      readPrompt('08_BEAR_CASE.md'),
      readPrompt('09_FINAL_RANKING.md'),
      readPrompt('99_OUTPUT_FORMATS.md'),
    ].join('\n\n---\n\n')

    const userMessage = `主题：${layer1.name}（${layer1.logic}）
卡脖子环节：${layer2.name}（${layer2.logic}）
卡脖子得分：${layer2.chokepointScore ?? '未知'}

请严格按照完整 Serenity 流程执行以下步骤，每一步的判断都影响最终输出：

1. 05_COMPANY_DISCOVERY
   - 识别直接暴露在该卡脖子环节的上市公司
   - 判断每家公司的 exposure_category（pure_play / high_exposure / partial_exposure）
   - 排除：OTC、SPAC、市值超 1000 亿美元的已充分定价龙头、与环节仅有 loose_exposure 的公司

2. 06_COMMERCIAL_VALIDATION
   - 对每家候选公司评估商业验证等级（0-3）和阶段标签
   - Level 0（无证据）直接淘汰，不出现在最终结果中
   - 须说明验证依据属于 hard/soft/inference

3. 07_FINANCIAL_VALUATION_CROWDING
   - 评估估值状态（undemanding/reasonable/stretched/very_stretched/unknown）
   - 评估机构拥挤度（low/medium/high/unknown）
   - 评估市场已重新定价程度（not_repriced/partially_repriced/mostly_repriced/unknown）
   - mostly_repriced + high crowding 的公司需降级或淘汰

4. 08_BEAR_CASE
   - 写出每家公司最有力的现实熊市论证（不是泛泛风险，是能打破论文的具体论点）
   - 判断是否 thesis-breaking，是则淘汰

5. 09_FINAL_RANKING
   - 按 7 维度综合打分（0-100）
   - 只保留 High Priority Research 或 Watchlist 级别
   - Wait for Pullback / Observe / Reject 不出现在最终输出中

最终输出 4-6 家公司，覆盖 A股/港股/美股，ticker 必须真实准确。

只返回 JSON，格式严格如下：
{
  "stocks": [
    {
      "id": "s1",
      "name": "公司全称",
      "ticker": "股票代码",
      "market": "A股 | 港股 | 美股",
      "exposureCategory": "pure_play | high_exposure | partial_exposure",
      "commercialValidationLevel": 2,
      "validationStageLabel": "Early Validation",
      "valuationStatus": "undemanding | reasonable | stretched | very_stretched | unknown",
      "crowdingStatus": "low | medium | high | unknown",
      "repricingStatus": "not_repriced | partially_repriced | mostly_repriced | unknown",
      "finalScore": 85,
      "classification": "High Priority Research | Watchlist",
      "oneSentenceThesis": "一句话说明为什么这家公司通过了全套 Serenity 筛选",
      "coreLogic": "在该卡脖子环节的具体位置和竞争优势（2-3句）",
      "bearCase": "最有力的现实熊市论证（1-2句，具体不泛泛）",
      "catalyst": "未来 6-24 个月最可能触发重新定价的具体催化剂"
    }
  ]
}`

    const data = await callOpenAI(systemPrompt, userMessage)
    return NextResponse.json(data)
  } catch (err) {
    console.error('[stocks]', err)
    return NextResponse.json({ error: '调用失败' }, { status: 500 })
  }
}
