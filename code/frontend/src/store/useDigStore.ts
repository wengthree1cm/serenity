'use client'

import { create } from 'zustand'
import type { Direction, Stock } from '@/types'

type Layer = 0 | 1 | 2 | 3

interface DigStore {
  layer: Layer
  loading: boolean
  error: string | null
  layer1Directions: Direction[]
  layer2Directions: Direction[]
  finalStocks: Stock[]
  selectedLayer1: Direction | null
  selectedLayer2: Direction | null

  startDig: () => Promise<void>
  selectLayer1: (direction: Direction) => Promise<void>
  selectLayer2: (direction: Direction) => Promise<void>
  digDeeper: () => Promise<void>
  reset: () => void
}

const API = process.env.NEXT_PUBLIC_API_URL ?? ''

async function post<T>(path: string, body?: unknown): Promise<T> {
  const res = await fetch(`${API}${path}`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: body ? JSON.stringify(body) : undefined,
  })
  if (!res.ok) throw new Error(`${res.status}`)
  return res.json()
}

export const useDigStore = create<DigStore>((set, get) => ({
  layer: 0,
  loading: false,
  error: null,
  layer1Directions: [],
  layer2Directions: [],
  finalStocks: [],
  selectedLayer1: null,
  selectedLayer2: null,

  startDig: async () => {
    set({ loading: true, error: null, layer: 1 })
    try {
      const data = await post<{ directions: Direction[] }>('/dig/layer1')
      set({ layer1Directions: data.directions, loading: false })
    } catch {
      set({ error: '加载失败，请重试', loading: false })
    }
  },

  selectLayer1: async (direction) => {
    set({ loading: true, error: null, selectedLayer1: direction, layer: 2 })
    try {
      const data = await post<{ directions: Direction[] }>('/dig/layer2', { direction })
      set({ layer2Directions: data.directions, loading: false })
    } catch {
      set({ error: '加载失败，请重试', loading: false })
    }
  },

  selectLayer2: async (direction) => {
    set({ loading: true, error: null, selectedLayer2: direction, layer: 3 })
    try {
      const data = await post<{ stocks: Stock[] }>('/dig/stocks', {
        layer1: get().selectedLayer1,
        layer2: direction,
      })
      set({ finalStocks: data.stocks, loading: false })
    } catch {
      set({ error: '加载失败，请重试', loading: false })
    }
  },

  digDeeper: async () => {
    const { selectedLayer1 } = get()
    if (!selectedLayer1) return
    set({ loading: true, error: null, layer: 2, layer2Directions: [], finalStocks: [], selectedLayer2: null })
    try {
      const data = await post<{ directions: Direction[] }>('/dig/layer2', {
        direction: selectedLayer1,
        deeper: true,
      })
      set({ layer2Directions: data.directions, loading: false })
    } catch {
      set({ error: '加载失败，请重试', loading: false })
    }
  },

  reset: () => {
    set({
      layer: 0,
      loading: false,
      error: null,
      layer1Directions: [],
      layer2Directions: [],
      finalStocks: [],
      selectedLayer1: null,
      selectedLayer2: null,
    })
  },
}))
