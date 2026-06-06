export interface Direction {
  id: string
  name: string
  logic: string
  exampleCompany?: string
  misunderstanding: string
}

export interface Stock {
  id: string
  name: string
  ticker: string
  market: 'A股' | '港股' | '美股'
  coreLogic: string
  catalyst: string
}
