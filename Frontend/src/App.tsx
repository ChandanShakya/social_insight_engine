import { useMemo, useState } from 'react'
import { fetchSentimentByPostId } from './services/sentimentService'
import type { SentimentSummary } from './types'

interface SearchHistory {
  postId: string
  timestamp: number
  summary: SentimentSummary
}

function App() {
  const [postId, setPostId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<SentimentSummary | null>(null)
  const [history, setHistory] = useState<SearchHistory[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [selectedTab, setSelectedTab] = useState<'all' | 'positive' | 'neutral' | 'negative'>('all')

  const canSearch = useMemo(() => postId.trim().length > 0 && !loading, [postId, loading])

  async function onSearch() {
    if (!canSearch) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetchSentimentByPostId(postId.trim())
      setData(res)
      setHistory(prev => [
        { postId: postId.trim(), timestamp: Date.now(), summary: res },
        ...prev.slice(0, 9) // Keep last 10
      ])
    } catch (e: any) {
      setError(e?.message || 'Failed to fetch sentiment')
    } finally {
      setLoading(false)
    }
  }

  function loadFromHistory(item: SearchHistory) {
    setPostId(item.postId)
    setData(item.summary)
    setError(null)
    setShowHistory(false)
  }

  function clearHistory() {
    setHistory([])
    setShowHistory(false)
  }

  const posW = data ? `${data.percentages.positive}%` : '0%'
  const neuW = data ? `${data.percentages.neutral}%` : '0%'
  const negW = data ? `${data.percentages.negative}%` : '0%'

  const filteredComments = useMemo(() => {
    if (!data) return []
    if (selectedTab === 'all') {
      return [
        ...data.comments.positive.map(c => ({ text: c, sentiment: 'positive' as const })),
        ...data.comments.neutral.map(c => ({ text: c, sentiment: 'neutral' as const })),
        ...data.comments.negative.map(c => ({ text: c, sentiment: 'negative' as const })),
      ]
    }
    return data.comments[selectedTab].map(c => ({ text: c, sentiment: selectedTab }))
  }, [data, selectedTab])

  const dominantSentiment = useMemo(() => {
    if (!data) return null
    const max = Math.max(data.percentages.positive, data.percentages.neutral, data.percentages.negative)
    if (max === data.percentages.positive) return 'positive'
    if (max === data.percentages.negative) return 'negative'
    return 'neutral'
  }, [data])

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 via-white to-purple-50">
      {/* Header */}
      <header className="bg-white border-b border-gray-200 shadow-sm sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                SocialInsight
              </h1>
              <p className="text-sm text-gray-600 mt-1">AI-Powered Social Media Sentiment Analysis</p>
            </div>
            <div className="flex items-center gap-4">
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="relative px-4 py-2 text-sm font-medium text-gray-700 hover:text-blue-600 transition-colors"
              >
                <svg className="w-5 h-5 inline mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                History
                {history.length > 0 && (
                  <span className="absolute -top-1 -right-1 bg-blue-600 text-white text-xs rounded-full w-5 h-5 flex items-center justify-center">
                    {history.length}
                  </span>
                )}
              </button>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-7xl mx-auto px-6 py-8">
        {/* Search Section */}
        <div className="bg-white rounded-2xl shadow-lg p-8 mb-8 border border-gray-100">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Analyze Post Sentiment</h2>
          <div className="flex gap-3">
            <input
              className="flex-1 px-4 py-3 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all"
              placeholder="Enter Post ID (e.g., 122098429155169978)"
              value={postId}
              onChange={(e) => setPostId(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter') onSearch()
              }}
            />
            <button
              className="px-8 py-3 bg-gradient-to-r from-blue-600 to-purple-600 text-white rounded-xl font-medium hover:from-blue-700 hover:to-purple-700 disabled:from-gray-300 disabled:to-gray-400 disabled:cursor-not-allowed transition-all shadow-md hover:shadow-lg disabled:shadow-none"
              disabled={!canSearch}
              onClick={onSearch}
            >
              {loading ? (
                <span className="flex items-center gap-2">
                  <svg className="animate-spin h-5 w-5" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                  </svg>
                  Analyzing...
                </span>
              ) : (
                'Analyze'
              )}
            </button>
          </div>
        </div>

        {/* History Dropdown */}
        {showHistory && history.length > 0 && (
          <div className="bg-white rounded-2xl shadow-lg p-6 mb-8 border border-gray-100">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Recent Searches</h3>
              <button
                onClick={clearHistory}
                className="text-sm text-red-600 hover:text-red-700 font-medium"
              >
                Clear All
              </button>
            </div>
            <div className="space-y-2 max-h-80 overflow-y-auto">
              {history.map((item, idx) => (
                <button
                  key={idx}
                  onClick={() => loadFromHistory(item)}
                  className="w-full text-left p-4 hover:bg-gray-50 rounded-lg transition-colors border border-gray-100"
                >
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-medium text-gray-900">Post: {item.postId}</div>
                      <div className="text-sm text-gray-600 mt-1">
                        {item.summary.total} comments • {new Date(item.timestamp).toLocaleString()}
                      </div>
                    </div>
                    <div className="flex gap-2 text-xs font-medium">
                      <span className="text-green-600">+{item.summary.percentages.positive}%</span>
                      <span className="text-gray-500">={item.summary.percentages.neutral}%</span>
                      <span className="text-red-600">-{item.summary.percentages.negative}%</span>
                    </div>
                  </div>
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Error Message */}
        {error && (
          <div className="p-4 mb-8 bg-red-50 border-2 border-red-200 rounded-xl shadow-sm flex items-start gap-3">
            <svg className="w-5 h-5 text-red-600 mt-0.5 flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
            </svg>
            <div>
              <h4 className="font-semibold text-red-900">Error</h4>
              <p className="text-red-700 text-sm mt-1">{error}</p>
            </div>
          </div>
        )}

        {/* Results */}
        {data && (
          <div className="space-y-8">
            {/* Overview Card */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h3 className="text-sm font-medium text-gray-600 mb-2">Analysis Results</h3>
                  <div className="text-4xl font-bold text-gray-900 mb-2">Post {data.postId}</div>
                  <div className="flex items-center gap-4 text-sm">
                    <span className="text-gray-600">{data.total} total comments</span>
                    {dominantSentiment && (
                      <span className={`px-3 py-1 rounded-full font-medium ${
                        dominantSentiment === 'positive' ? 'bg-green-100 text-green-700' :
                        dominantSentiment === 'negative' ? 'bg-red-100 text-red-700' :
                        'bg-gray-100 text-gray-700'
                      }`}>
                        Mostly {dominantSentiment}
                      </span>
                    )}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm text-gray-600 mb-1">Overall Sentiment</div>
                  <div className={`text-3xl font-bold ${
                    dominantSentiment === 'positive' ? 'text-green-600' :
                    dominantSentiment === 'negative' ? 'text-red-600' :
                    'text-gray-600'
                  }`}>
                    {dominantSentiment === 'positive' ? '😊' :
                     dominantSentiment === 'negative' ? '😔' : '😐'}
                  </div>
                </div>
              </div>

              {/* Progress Bar */}
              <div className="mb-6">
                <div className="flex h-4 rounded-full overflow-hidden shadow-inner mb-3" aria-label="Sentiment distribution">
                  <div className="bg-gradient-to-r from-green-400 to-green-500 transition-all duration-500" style={{ width: posW }} />
                  <div className="bg-gradient-to-r from-gray-400 to-gray-500 transition-all duration-500" style={{ width: neuW }} />
                  <div className="bg-gradient-to-r from-red-400 to-red-500 transition-all duration-500" style={{ width: negW }} />
                </div>
                <div className="flex justify-between text-sm font-semibold">
                  <span className="text-green-600">Positive {data.percentages.positive}%</span>
                  <span className="text-gray-600">Neutral {data.percentages.neutral}%</span>
                  <span className="text-red-600">Negative {data.percentages.negative}%</span>
                </div>
              </div>

              {/* Stats Grid as mini bar charts */}
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="p-4 bg-green-50 rounded-xl border border-green-100">
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-sm font-medium text-green-700">Positive ({data.counts.positive})</span>
                    <span className="text-sm font-semibold text-green-700">{data.percentages.positive}%</span>
                  </div>
                  <div className="h-2 w-full bg-green-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-green-500 transition-all duration-500"
                      style={{ width: `${data.percentages.positive}%` }}
                    />
                  </div>
                </div>
                <div className="p-4 bg-gray-50 rounded-xl border border-gray-200">
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-sm font-medium text-gray-700">Neutral ({data.counts.neutral})</span>
                    <span className="text-sm font-semibold text-gray-700">{data.percentages.neutral}%</span>
                  </div>
                  <div className="h-2 w-full bg-gray-200 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-gray-500 transition-all duration-500"
                      style={{ width: `${data.percentages.neutral}%` }}
                    />
                  </div>
                </div>
                <div className="p-4 bg-red-50 rounded-xl border border-red-100">
                  <div className="flex items-baseline justify-between mb-2">
                    <span className="text-sm font-medium text-red-700">Negative ({data.counts.negative})</span>
                    <span className="text-sm font-semibold text-red-700">{data.percentages.negative}%</span>
                  </div>
                  <div className="h-2 w-full bg-red-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-red-500 transition-all duration-500"
                      style={{ width: `${data.percentages.negative}%` }}
                    />
                  </div>
                </div>
              </div>
            </div>

            {/* Comments Section */}
            <div className="bg-white rounded-2xl shadow-lg p-8 border border-gray-100">
              <h3 className="text-xl font-semibold text-gray-900 mb-6">Comment Analysis</h3>
              
              {/* Tabs */}
              <div className="flex gap-2 mb-6 border-b border-gray-200">
                {(['all', 'positive', 'neutral', 'negative'] as const).map(tab => (
                  <button
                    key={tab}
                    onClick={() => setSelectedTab(tab)}
                    className={`px-4 py-2 font-medium text-sm capitalize transition-colors border-b-2 ${
                      selectedTab === tab
                        ? 'border-blue-600 text-blue-600'
                        : 'border-transparent text-gray-600 hover:text-gray-900'
                    }`}
                  >
                    {tab}
                    {tab !== 'all' && ` (${data.counts[tab]})`}
                  </button>
                ))}
              </div>

              {/* Comments List */}
              <div className="space-y-3 max-h-96 overflow-y-auto pr-2">
                {filteredComments.length === 0 ? (
                  <div className="text-center py-8 text-gray-500">
                    No comments in this category
                  </div>
                ) : (
                  filteredComments.map((comment, idx) => (
                    <div
                      key={idx}
                      className={`p-4 rounded-lg border-l-4 ${
                        comment.sentiment === 'positive'
                          ? 'bg-green-50 border-green-500'
                          : comment.sentiment === 'negative'
                          ? 'bg-red-50 border-red-500'
                          : 'bg-gray-50 border-gray-400'
                      }`}
                    >
                      <div className="flex items-start gap-3">
                        <span className="text-lg">
                          {comment.sentiment === 'positive' ? '😊' :
                           comment.sentiment === 'negative' ? '😔' : '😐'}
                        </span>
                        <p className="flex-1 text-gray-800 text-sm leading-relaxed">{comment.text}</p>
                      </div>
                    </div>
                  ))
                )}
              </div>
            </div>
          </div>
        )}

        {/* Empty State */}
        {!data && !error && !loading && (
          <div className="text-center py-16">
            <div className="text-6xl mb-4">🔍</div>
            <h3 className="text-xl font-semibold text-gray-900 mb-2">Ready to Analyze</h3>
            <p className="text-gray-600">Enter a post ID above to get started with sentiment analysis</p>
          </div>
        )}
      </div>

      {/* Footer */}
      <footer className="mt-16 border-t border-gray-200 bg-white">
        <div className="max-w-7xl mx-auto px-6 py-8 text-center text-sm text-gray-600">
          <p>Powered by AI • Real-time Sentiment Analysis • SocialInsight Engine</p>
        </div>
      </footer>
    </div>
  )
}

export default App
