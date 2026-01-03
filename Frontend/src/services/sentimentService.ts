import type { SentimentSummary, SentimentLabel } from '../types'

function round2(n: number) {
  return Math.round(n * 100) / 100
}

// Fetch classification from backend and adapt to SentimentSummary
export async function fetchSentimentByPostId(postId: string): Promise<SentimentSummary> {
  const url = 'http://localhost:8000/classify'
  const res = await fetch(url)
  if (!res.ok) {
    throw new Error(`Backend error (${res.status}) while fetching classification`)
  }

  const payload = await res.json().catch(() => ({ data: [] }))
  const rows: any[] = Array.isArray(payload?.data) ? payload.data : []

  const counts: Record<SentimentLabel, number> = { positive: 0, neutral: 0, negative: 0 }
  const comments: Record<SentimentLabel, string[]> = { positive: [], neutral: [], negative: [] }

  for (const row of rows) {
    const raw = String(row?.sentiments ?? row?.sentiment ?? '').trim().toUpperCase()
    const text = String(row?.Comments ?? row?.comment ?? '')
    const labelMap: Record<string, SentimentLabel> = {
      POS: 'positive',
      NEG: 'negative',
      NEU: 'neutral',
      POSITIVE: 'positive',
      NEGATIVE: 'negative',
      NEUTRAL: 'neutral',
    }
    const label: SentimentLabel = labelMap[raw] ?? 'neutral'
    counts[label] += 1
    if (text) comments[label].push(text)
  }

  const total = rows.length
  const percentages: Record<SentimentLabel, number> = {
    positive: total ? round2((counts.positive / total) * 100) : 0,
    neutral: total ? round2((counts.neutral / total) * 100) : 0,
    negative: total ? round2((counts.negative / total) * 100) : 0,
  }

  return { postId, total, counts, percentages, comments }
}
