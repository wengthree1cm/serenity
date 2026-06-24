import OpenAI from 'openai'
import fs from 'fs'
import path from 'path'

export const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

// 本地: code/frontend/ → ../../gpt/prompts
// Vercel: outputFileTracingRoot 把 gpt/prompts 打包到 serverless bundle 里，
//         路径仍然是相对于 code/frontend 的 ../../gpt/prompts
function resolvePromptsDir(): string {
  const candidates = [
    path.join(process.cwd(), '../../gpt/prompts'),  // 本地开发 & Vercel bundle
    path.join(process.cwd(), 'gpt/prompts'),         // 备用
  ]
  for (const dir of candidates) {
    if (fs.existsSync(dir)) return dir
  }
  return candidates[0]
}

const PROMPTS_DIR = resolvePromptsDir()

export function readPrompt(filename: string): string {
  return fs.readFileSync(path.join(PROMPTS_DIR, filename), 'utf-8')
}

export async function callOpenAI(systemPrompt: string, userMessage: string): Promise<unknown> {
  const response = await openai.chat.completions.create({
    model: 'gpt-4o',
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userMessage },
    ],
    response_format: { type: 'json_object' },
    temperature: 0.7,
  })
  return JSON.parse(response.choices[0].message.content!)
}
