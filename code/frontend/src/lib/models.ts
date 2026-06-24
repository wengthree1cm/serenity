export interface ModelOption {
  id: string
  label: string
  desc: string
  tier: 'cheap' | 'balanced' | 'best'
}

export const MODELS: ModelOption[] = [
  {
    id: 'gpt-4o-mini',
    label: 'GPT-4o Mini',
    desc: '便宜快速，适合快速验证',
    tier: 'cheap',
  },
  {
    id: 'gpt-4.1-mini',
    label: 'GPT-4.1 Mini',
    desc: '新一代轻量，性价比高',
    tier: 'cheap',
  },
  {
    id: 'gpt-4o',
    label: 'GPT-4o',
    desc: '均衡主力，当前默认',
    tier: 'balanced',
  },
  {
    id: 'gpt-4.1',
    label: 'GPT-4.1',
    desc: '旗舰模型，分析更深',
    tier: 'best',
  },
  {
    id: 'o4-mini',
    label: 'o4-mini',
    desc: '深度推理，最适合投资分析',
    tier: 'best',
  },
]

export const DEFAULT_MODEL = 'gpt-4o'
