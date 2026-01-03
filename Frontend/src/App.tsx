import { useMemo, useState } from 'react'
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
    <div className="max-w-4xl mx-auto p-6">
      <h1 className="text-4xl font-bold text-gray-900 mb-2">SocialInsight</h1>
      <p className="text-sm text-gray-600 mb-4">Search sentiment by Post ID</p>

      <div className="flex gap-3 mb-6">
        <input
          className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          placeholder="Enter Post ID (e.g., 12345)"
          value={postId}
          onChange={(e) => setPostId(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === 'Enter') onSearch()
          }}
        />
        <button
          className="px-6 py-2 bg-blue-600 text-white rounded-lg font-medium hover:bg-blue-700 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
          disabled={!canSearch}
          onClick={onSearch}
        >
          {loading ? 'Searching…' : 'Search'}
        </button>
      </div>

      {error && (
        <div className="p-4 mb-6 bg-white border-2 border-red-500 rounded-lg shadow-sm">
          {error}
        </div>
      )}

      {data && (
        <div>
          <div className="p-6 mb-6 bg-white border border-gray-200 rounded-lg shadow-sm">
            <div className="text-sm text-gray-600 mb-2">Post</div>
            <div className="flex justify-between items-baseline gap-3 mb-4">
              <div className="text-3xl font-bold text-gray-900">{data.postId}</div>
              <div className="text-sm text-gray-600">{data.total} comments</div>
            </div>
            <div className="flex h-2 rounded-full overflow-hidden mb-3" aria-label="Sentiment distribution">
              <div className="bg-green-500" style={{ width: posW }} />
              <div className="bg-gray-400" style={{ width: neuW }} />
              <div className="bg-red-500" style={{ width: negW }} />
            </div>
            <div className="flex gap-4 text-sm font-medium">
              <span className="text-green-500">+{data.percentages.positive}%</span>
              <span className="text-gray-400">= {data.percentages.neutral}%</span>
              <span className="text-red-500">- {data.percentages.negative}%</span>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="text-sm text-gray-600 mb-2">Positive ({data.counts.positive})</div>
              <div className="text-3xl font-bold text-gray-900 mb-4">{data.percentages.positive}%</div>
              <ul className="space-y-2 text-sm text-gray-700">
                {data.comments.positive.map((c, i) => (
                  <li key={`p-${i}`} className="list-disc list-inside">{c}</li>
                ))}
              </ul>
            </div>
            <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="text-sm text-gray-600 mb-2">Neutral ({data.counts.neutral})</div>
              <div className="text-3xl font-bold text-gray-900 mb-4">{data.percentages.neutral}%</div>
              <ul className="space-y-2 text-sm text-gray-700">
                {data.comments.neutral.map((c, i) => (
                  <li key={`n-${i}`} className="list-disc list-inside">{c}</li>
                ))}
              </ul>
            </div>
            <div className="p-6 bg-white border border-gray-200 rounded-lg shadow-sm">
              <div className="text-sm text-gray-600 mb-2">Negative ({data.counts.negative})</div>
              <div className="text-3xl font-bold text-gray-900 mb-4">{data.percentages.negative}%</div>
              <ul className="space-y-2 text-sm text-gray-700">
                {data.comments.negative.map((c, i) => (
                  <li key={`m-${i}`} className="list-disc list-inside">{c}</li>
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
