import { useMemo, useState } from 'react'
import './App.css'
import { fetchSentimentByPostId } from './services/sentimentService'
import type { SentimentSummary } from './types'

function App() {
  const [postId, setPostId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<SentimentSummary | null>(null)

  const canSearch = useMemo(() => postId.trim().length > 0 && !loading, [postId, loading])

  async function onSearch() {
    if (!canSearch) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetchSentimentByPostId(postId.trim())
      setData(res)
    } catch (e: any) {
      setError(e?.message || 'Failed to fetch sentiment')
    } finally {
      setLoading(false)
    }
  }

  const posW = data ? `${data.percentages.positive}%` : '0%'
  const neuW = data ? `${data.percentages.neutral}%` : '0%'
  const negW = data ? `${data.percentages.negative}%` : '0%'

  return (
    <div className="container">
      <h1>SocialInsight</h1>
      <p className="label">Search sentiment by Post ID</p>

      <div className="searchRow">
        <input
          className="input"
          placeholder="Enter Post ID (e.g., 12345)"
          value={postId}
          onChange={(e) => setPostId(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') onSearch()
          }}
        />
        <button className="btn" disabled={!canSearch} onClick={onSearch}>
          {loading ? 'Searching…' : 'Search'}
        </button>
      </div>

      {error && <div className="cardBox" style={{ borderColor: '#ef4444' }}>{error}</div>}

      {data && (
        <div>
          <div className="cardBox">
            <div className="label">Post</div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', gap: 12 }}>
              <div className="kpi">{data.postId}</div>
              <div className="label">{data.total} comments</div>
            </div>
            <div className="bar" aria-label="Sentiment distribution">
              <div className="barPos" style={{ width: posW }} />
              <div className="barNeu" style={{ width: neuW }} />
              <div className="barNeg" style={{ width: negW }} />
            </div>
            <div style={{ display: 'flex', gap: 16, marginTop: 8 }}>
              <span style={{ color: '#22c55e' }}>+{data.percentages.positive}%</span>
              <span style={{ color: '#9ca3af' }}>= {data.percentages.neutral}%</span>
              <span style={{ color: '#ef4444' }}>- {data.percentages.negative}%</span>
            </div>
          </div>

          <div className="summaryGrid">
            <div className="cardBox">
              <div className="label">Positive ({data.counts.positive})</div>
              <div className="kpi">{data.percentages.positive}%</div>
              <ul className="list">
                {data.comments.positive.map((c, i) => (
                  <li key={`p-${i}`}>{c}</li>
                ))}
              </ul>
            </div>
            <div className="cardBox">
              <div className="label">Neutral ({data.counts.neutral})</div>
              <div className="kpi">{data.percentages.neutral}%</div>
              <ul className="list">
                {data.comments.neutral.map((c, i) => (
                  <li key={`n-${i}`}>{c}</li>
                ))}
              </ul>
            </div>
            <div className="cardBox">
              <div className="label">Negative ({data.counts.negative})</div>
              <div className="kpi">{data.percentages.negative}%</div>
              <ul className="list">
                {data.comments.negative.map((c, i) => (
                  <li key={`m-${i}`}>{c}</li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default App
