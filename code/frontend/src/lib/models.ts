export interface ModelOption {
  id: string
  label: string
  desc: string
  tier: 'cheap' | 'balanced' | 'best'
}

export const MODELS: ModelOption[] = [
  {
    id: 'gpt-4.1-nano',
    label: 'GPT-4.1 Nano',
    desc: '最便宜，测试用',
    tier: 'cheap',
  },
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
    desc: '最新旗舰，分析更深',
    tier: 'best',
  },
  {
    id: 'o3-mini',
    label: 'o3-mini',
    desc: '推理模型，比 o4-mini 便宜',
    tier: 'best',
  },
  {
    id: 'o4-mini',
    label: 'o4-mini',
    desc: '最强推理，最适合投资分析',
    tier: 'best',
  },
]

export const DEFAULT_MODEL = 'gpt-4o'
