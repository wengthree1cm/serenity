import OpenAI from 'openai'
import fs from 'fs'
import path from 'path'
import { DEFAULT_MODEL } from './models'

export const openai = new OpenAI({ apiKey: process.env.OPENAI_API_KEY })

function resolvePromptsDir(): string {
  const candidates = [
    path.join(process.cwd(), '../../gpt/prompts'),
    path.join(process.cwd(), 'gpt/prompts'),
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

export async function callOpenAI(
  systemPrompt: string,
  userMessage: string,
  model: string = DEFAULT_MODEL,
): Promise<unknown> {
  const isReasoning = model.startsWith('o')

  const response = await openai.chat.completions.create({
    model,
    messages: [
      { role: 'system', content: systemPrompt },
      { role: 'user', content: userMessage },
    ],
    response_format: { type: 'json_object' },
    // 推理模型（o系列）不支持 temperature
    ...(!isReasoning && { temperature: 0.7 }),
  })

  return JSON.parse(response.choices[0].message.content!)
}
