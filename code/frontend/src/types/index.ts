export interface Direction {
  id: string
  name: string
  logic: string
  exampleCompany?: string
  misunderstanding: string
  chokepointScore?: number  // layer2 才有，来自 04_CHOKEPOINT_SCORING
}

export type Market = 'A股' | '港股' | '美股'

export type ExposureCategory =
  | 'pure_play'
  | 'high_exposure'
  | 'partial_exposure'

export type Classification =
  | 'High Priority Research'
  | 'Watchlist'
  | 'Wait for Pullback'
  | 'Observe'

export type ValuationStatus =
  | 'undemanding'
  | 'reasonable'
  | 'stretched'
  | 'very_stretched'
  | 'unknown'

export type CrowdingStatus = 'low' | 'medium' | 'high' | 'unknown'

export type RepricingStatus =
  | 'not_repriced'
  | 'partially_repriced'
  | 'mostly_repriced'
  | 'unknown'

export interface Stock {
  id: string
  name: string
  ticker: string
  market: Market

  // 来自 05_COMPANY_DISCOVERY
  exposureCategory: ExposureCategory

  // 来自 06_COMMERCIAL_VALIDATION
  commercialValidationLevel: 0 | 1 | 2 | 3
  validationStageLabel: string

  // 来自 07_FINANCIAL_VALUATION_CROWDING
  valuationStatus: ValuationStatus
  crowdingStatus: CrowdingStatus
  repricingStatus: RepricingStatus

  // 来自 09_FINAL_RANKING
  finalScore: number
  classification: Classification
  oneSentenceThesis: string

  // 来自 08_BEAR_CASE
  bearCase: string

  // 核心输出
  coreLogic: string
  catalyst: string
}
