import type { SentimentSummary, SentimentLabel } from '../types'

// Deterministic pseudo-random generator for consistent mock results per postId
function seededRandom(seed: string) {
  let h = 2166136261 >>> 0
  for (let i = 0; i < seed.length; i++) {
    h ^= seed.charCodeAt(i)
    h = Math.imul(h, 16777619)
  }
  return () => {
    h += 0x6D2B79F5
    let t = Math.imul(h ^ (h >>> 15), 1 | h)
    t ^= t + Math.imul(t ^ (t >>> 7), 61 | t)
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296
  }
}

function round2(n: number) {
  return Math.round(n * 100) / 100
}

export async function fetchSentimentByPostId(postId: string): Promise<SentimentSummary> {
  const rand = seededRandom(postId.trim().toLowerCase() || 'default')

  // Create mock counts that always sum to total
  const total = 20 + Math.floor(rand() * 80) // 20-99 comments
  // Start with proportions then scale to counts
  let pPos = 0.2 + rand() * 0.6 // 0.2-0.8
  let pNeg = 0.1 + rand() * (0.9 - pPos) // ensure sum < 1
  // pNeu is implied; we'll compute neutral count to make totals align

  // Convert to integer counts
  let pos = Math.max(0, Math.floor(total * pPos))
  let neg = Math.max(0, Math.floor(total * pNeg))
  let neu = Math.max(0, total - pos - neg)

  // Comments per sentiment (up to 5 each)
  const makeComments = (label: SentimentLabel, count: number) => {
    const limit = Math.min(5, Math.max(1, Math.floor(count / 3)))
    const samples: Record<SentimentLabel, string[]> = {
      positive: [
        'Loved this! Super insightful.',
        'Great post—very helpful.',
        'Absolutely agree, well said.',
        'This made my day!',
        'Positive vibes only.'
      ],
      neutral: [
        'Interesting point.',
        'Thanks for sharing.',
        'Noted.',
        'Okay.',
        'Neutral on this.'
      ],
      negative: [
        'Not convinced about this.',
        "I don't agree.",
        'This seems off.',
        'Disappointed with the take.',
        'Could be better.'
      ]
    }
    const arr = samples[label]
    const out: string[] = []
    for (let i = 0; i < limit; i++) {
      out.push(arr[Math.floor(rand() * arr.length)])
    }
    return out
  }

  const counts = { positive: pos, neutral: neu, negative: neg } as const
  const percentages = {
    positive: round2((counts.positive / total) * 100),
    neutral: round2((counts.neutral / total) * 100),
    negative: round2((counts.negative / total) * 100)
  }

  const comments = {
    positive: makeComments('positive', counts.positive),
    neutral: makeComments('neutral', counts.neutral),
    negative: makeComments('negative', counts.negative)
  }

  // Simulate network delay
  await new Promise((r) => setTimeout(r, 500 + Math.floor(rand() * 800)))

  return {
    postId,
    total,
    counts: { ...counts },
    percentages,
    comments
  }
}
