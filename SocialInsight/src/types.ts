export type SentimentLabel = 'positive' | 'neutral' | 'negative'

export interface SentimentSummary {
  postId: string
  total: number
  counts: Record<SentimentLabel, number>
  percentages: Record<SentimentLabel, number>
  comments: Record<SentimentLabel, string[]>
}
