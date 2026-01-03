import { useMemo, useState } from 'react'
import { fetchSentimentByPostId } from './services/sentimentService'
import type { SentimentSummary } from './types'
import { useTheme } from './services/themeService'
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  PieChart, Pie, Cell, Legend
} from 'recharts'
import {
  Search, Sun, Moon, MessageSquare, PieChart as PieIcon,
  ThumbsUp, ThumbsDown, Minus, AlertCircle, ChevronLeft, ChevronRight,
  TrendingUp, LayoutDashboard, Database, Info, Lightbulb, Sparkles, ShieldAlert
} from 'lucide-react'
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}

interface SearchHistory {
  postId: string
  timestamp: number
  summary: SentimentSummary
}

function App() {
  const { theme, setTheme } = useTheme()
  const [postId, setPostId] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [data, setData] = useState<SentimentSummary | null>(null)
  const [history, setHistory] = useState<SearchHistory[]>([])
  const [showHistory, setShowHistory] = useState(false)
  const [currentPage, setCurrentPage] = useState(1)
  const [selectedTab, setSelectedTab] = useState<'all' | 'positive' | 'neutral' | 'negative'>('all')

  const commentsPerPage = 5

  const canSearch = useMemo(() => postId.trim().length > 0 && !loading, [postId, loading])

  async function onSearch() {
    if (!canSearch) return
    setLoading(true)
    setError(null)
    try {
      const res = await fetchSentimentByPostId(postId.trim())
      setData(res)
      const newHistoryItem = { postId: postId.trim(), timestamp: Date.now(), summary: res }
      setHistory(prev => {
        const filtered = prev.filter(h => h.postId !== postId.trim()) // Avoid duplicates, move to top
        return [newHistoryItem, ...filtered.slice(0, 9)]
      })
      setCurrentPage(1)
      setShowHistory(false)
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
    setCurrentPage(1)
  }

  function clearHistory() {
    setHistory([])
    setShowHistory(false)
  }

  const pieData = useMemo(() => {
    if (!data) return []
    return [
      { name: 'Positive', value: data.counts.positive, color: '#10b981' },
      { name: 'Neutral', value: data.counts.neutral, color: '#71717a' },
      { name: 'Negative', value: data.counts.negative, color: '#f43f5e' },
    ]
  }, [data])

  const barData = useMemo(() => {
    if (!data) return []
    return [
      { name: 'Positive', value: data.counts.positive, fill: '#10b981' },
      { name: 'Neutral', value: data.counts.neutral, fill: '#71717a' },
      { name: 'Negative', value: data.counts.negative, fill: '#f43f5e' },
    ]
  }, [data])

  const filteredComments = useMemo(() => {
    if (!data) return []
    let all: { text: string; sentiment: 'positive' | 'neutral' | 'negative' }[] = []

    if (selectedTab === 'all' || selectedTab === 'positive') {
      all.push(...data.comments.positive.map(c => ({ text: c, sentiment: 'positive' as const })))
    }
    if (selectedTab === 'all' || selectedTab === 'neutral') {
      all.push(...data.comments.neutral.map(c => ({ text: c, sentiment: 'neutral' as const })))
    }
    if (selectedTab === 'all' || selectedTab === 'negative') {
      all.push(...data.comments.negative.map(c => ({ text: c, sentiment: 'negative' as const })))
    }

    return all
  }, [data, selectedTab])

  const paginatedComments = useMemo(() => {
    const start = (currentPage - 1) * commentsPerPage
    return filteredComments.slice(start, start + commentsPerPage)
  }, [filteredComments, currentPage])

  const totalPages = Math.ceil(filteredComments.length / commentsPerPage)

  function TakeawayList({ items, type }: { items: string[]; type: 'positive' | 'negative' }) {
    return (
      <div className="space-y-4">
        {items.map((item, idx) => {
          const trimmedItem = item.trim();
          if (!trimmedItem) return null;

          const isBullet = trimmedItem.startsWith('*');
          const cleanItem = isBullet ? trimmedItem.substring(1).trim() : trimmedItem;

          // Robust regex for **bold** text
          const parts = cleanItem.split(/(\*\*.*?\*\*)/g);

          return (
            <div key={idx} className={cn(
              "flex gap-3",
              isBullet ? "pl-2" : "mt-8 first:mt-0"
            )}>
              {isBullet ? (
                <div className={cn(
                  "w-1.5 h-1.5 rounded-full mt-[9px] shrink-0 shadow-sm",
                  type === 'positive' ? "bg-emerald-500" : "bg-rose-500"
                )} />
              ) : null}
              <div className="flex-1">
                <p className={cn(
                  "leading-relaxed tracking-normal",
                  !isBullet
                    ? "font-black text-foreground/60 uppercase tracking-widest text-[10px] sm:text-xs flex items-center gap-2 mb-2"
                    : "text-sm md:text-[15px] text-muted-foreground font-medium"
                )}>
                  {!isBullet && (type === 'positive' ? <Sparkles className="w-3.5 h-3.5" /> : <ShieldAlert className="w-3.5 h-3.5" />)}
                  <span className="inline-block align-middle">
                    {parts.map((part, i) => {
                      if (part.startsWith('**') && part.endsWith('**')) {
                        return <strong key={i} className="font-bold text-foreground">{part.slice(2, -2)}</strong>;
                      }
                      return part;
                    })}
                  </span>
                </p>
              </div>
            </div>
          );
        })}
      </div>
    );
  }

  return (
    <div className="min-h-screen flex flex-col transition-colors duration-300">
      {/* Navbar */}
      <nav className="border-b border-border bg-card/80 backdrop-blur-md sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-primary text-primary-foreground rounded-xl shadow-lg">
              <MessageSquare className="w-5 h-5" />
            </div>
            <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-foreground to-muted-foreground bg-clip-text text-transparent">
              SocialInsight
            </span>
          </div>

          <div className="flex items-center gap-2">
            {history.length > 0 && (
              <button
                onClick={() => setShowHistory(!showHistory)}
                className="p-2.5 hover:bg-secondary rounded-xl transition-all border border-transparent hover:border-border relative"
                title="Search History"
              >
                <TrendingUp className="w-5 h-5" />
                <span className="absolute -top-1 -right-1 bg-primary text-primary-foreground text-[10px] font-black w-4 h-4 rounded-full flex items-center justify-center border-2 border-card">
                  {history.length}
                </span>
              </button>
            )}
            <button
              onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
              className="p-2.5 hover:bg-secondary rounded-xl transition-all active:scale-95 border border-transparent hover:border-border"
              title={`Switch to ${theme === 'dark' ? 'light' : 'dark'} mode`}
            >
              {theme === 'dark' ? <Sun className="w-5 h-5 text-amber-400" /> : <Moon className="w-5 h-5 text-blue-600" />}
            </button>
          </div>
        </div>
      </nav>

      {/* Main Content Area */}
      <main className="flex-grow max-w-7xl mx-auto w-full px-4 sm:px-6 py-8 md:py-16">
        {/* History Dropdown Panel */}
        {showHistory && history.length > 0 && (
          <div className="max-w-3xl mx-auto mb-12 animate-in slide-in-from-top-4 duration-300">
            <div className="bg-card border border-border rounded-3xl p-6 shadow-2xl">
              <div className="flex items-center justify-between mb-6">
                <h3 className="font-black text-lg flex items-center gap-2">
                  <TrendingUp className="w-5 h-5 text-primary" />
                  Recent Searches
                </h3>
                <button onClick={clearHistory} className="text-xs font-black uppercase tracking-widest text-destructive hover:opacity-70 transition-opacity">
                  Clear History
                </button>
              </div>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-3 max-h-[400px] overflow-y-auto no-scrollbar pr-2">
                {history.map((item, idx) => (
                  <button
                    key={idx}
                    onClick={() => loadFromHistory(item)}
                    className="text-left p-4 bg-muted/20 border border-border hover:border-primary/30 rounded-2xl transition-all group"
                  >
                    <div className="flex flex-col gap-1">
                      <span className="text-sm font-black group-hover:text-primary transition-colors">Post: {item.postId}</span>
                      <span className="text-[10px] font-bold text-muted-foreground uppercase">
                        {new Date(item.timestamp).toLocaleString([], { dateStyle: 'medium', timeStyle: 'short' })}
                      </span>
                    </div>
                  </button>
                ))}
              </div>
            </div>
          </div>
        )}
        <div className="flex flex-col items-center text-center mb-10 md:mb-16">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-primary/5 border border-primary/10 text-primary text-xs font-bold mb-6 animate-fade-in">
            <TrendingUp className="w-3 h-3" />
            <span>AI-POWERED ANALYSIS</span>
          </div>
          <h1 className="text-4xl md:text-6xl font-black mb-6 tracking-tight">
            Customer Sentiment <span className="text-primary">Analysis</span>
          </h1>
          <p className="text-muted-foreground text-base md:text-xl max-w-2xl leading-relaxed">
            Instantly understand how your customers feel. Enter a Facebook Post ID to analyze sentiment distribution and feedback patterns.
          </p>
        </div>

        {/* Search Section */}
        <div className="max-w-3xl mx-auto mb-16 md:mb-24">
          <div className="bg-card border border-border rounded-2xl md:rounded-3xl p-2 md:p-3 flex flex-col md:flex-row items-center gap-2 shadow-2xl relative z-10">
            <div className="hidden md:flex pl-4 text-muted-foreground">
              <Database className="w-5 h-5" />
            </div>
            <input
              className="w-full md:flex-1 bg-transparent border-none focus:ring-0 text-base md:text-lg py-3 px-4 outline-none placeholder:text-muted-foreground/50"
              placeholder="Paste Facebook Post ID here..."
              value={postId}
              onChange={(e) => setPostId(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && onSearch()}
            />
            <button
              onClick={onSearch}
              disabled={!canSearch}
              className={cn(
                "w-full md:w-auto px-8 py-4 rounded-xl md:rounded-2xl font-bold flex items-center justify-center gap-3 transition-all active:scale-[0.98]",
                canSearch
                  ? "bg-primary text-primary-foreground hover:opacity-90 shadow-xl shadow-primary/20"
                  : "bg-muted text-muted-foreground cursor-not-allowed"
              )}
            >
              {loading ? (
                <div className="w-5 h-5 border-3 border-primary-foreground border-t-transparent animate-spin rounded-full" />
              ) : (
                <Search className="w-5 h-5" />
              )}
              {loading ? 'Analyzing...' : 'Analyze Now'}
            </button>
          </div>
          {error && (
            <div className="mt-6 flex items-start gap-3 text-destructive bg-destructive/5 p-5 rounded-2xl border border-destructive/20 animate-in slide-in-from-top-2">
              <AlertCircle className="w-5 h-5 mt-0.5 shrink-0" />
              <div className="flex flex-col">
                <span className="text-sm font-bold">Analysis Failed</span>
                <span className="text-sm opacity-90">{error}</span>
              </div>
            </div>
          )}
        </div>

        {!data && !loading && (
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 md:gap-8 max-w-5xl mx-auto">
            {[
              { icon: TrendingUp, title: "Sentiment Trends", desc: "Identify positive and negative shifts instantly" },
              { icon: LayoutDashboard, title: "Visual Reports", desc: "Understand distribution through clear charts" },
              { icon: Info, title: "Granular Feedback", desc: "Read individual comments filtered by sentiment" },
            ].map((feature, i) => (
              <div key={i} className="p-8 bg-card/50 border border-border rounded-3xl flex flex-col items-center text-center group hover:bg-card hover:border-primary/20 transition-all duration-300">
                <div className="w-14 h-14 rounded-2xl bg-secondary flex items-center justify-center mb-6 group-hover:scale-110 group-hover:bg-primary group-hover:text-primary-foreground transition-all duration-300 shadow-sm">
                  <feature.icon className="w-7 h-7" />
                </div>
                <h3 className="font-bold text-lg mb-3 tracking-tight">{feature.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed font-medium">{feature.desc}</p>
              </div>
            ))}
          </div>
        )}

        {data && (
          <div className="space-y-8 md:space-y-12 animate-in fade-in slide-in-from-bottom-8 duration-700">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 md:gap-6">
              {[
                { label: 'Positive', count: data.counts.positive, perc: data.percentages.positive, color: 'text-emerald-500', icon: ThumbsUp, bg: 'bg-emerald-500/10', border: 'border-emerald-500/20' },
                { label: 'Neutral', count: data.counts.neutral, perc: data.percentages.neutral, color: 'text-zinc-500', icon: Minus, bg: 'bg-zinc-500/10', border: 'border-zinc-500/20' },
                { label: 'Negative', count: data.counts.negative, perc: data.percentages.negative, color: 'text-rose-500', icon: ThumbsDown, bg: 'bg-rose-500/10', border: 'border-rose-500/20' },
              ].map((stat, i) => (
                <div key={i} className={cn("bg-card border p-8 rounded-3xl transition-all hover:shadow-xl", stat.border)}>
                  <div className="flex items-center justify-between mb-6">
                    <span className="text-sm font-bold text-muted-foreground uppercase tracking-widest">{stat.label}</span>
                    <div className={cn("p-2.5 rounded-xl", stat.bg)}>
                      <stat.icon className={cn("w-5 h-5", stat.color)} />
                    </div>
                  </div>
                  <div className="flex items-end justify-between">
                    <div className="flex flex-col">
                      <span className="text-4xl font-black">{stat.count}</span>
                      <span className="text-xs text-muted-foreground font-medium mt-1">Total Comments</span>
                    </div>
                    <div className={cn("text-xl font-black italic", stat.color)}>
                      {stat.perc}%
                    </div>
                  </div>
                </div>
              ))}
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
              {/* Sentiment Distribution Pie */}
              <div className="bg-card border border-border p-6 md:p-8 rounded-3xl shadow-sm">
                <div className="flex items-center gap-2 mb-8">
                  <PieIcon className="w-5 h-5 text-primary" />
                  <h3 className="font-bold text-lg">Overall Distribution</h3>
                </div>
                <div className="h-[280px] md:h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <PieChart>
                      <Pie
                        data={pieData}
                        cx="50%"
                        cy="50%"
                        innerRadius={80}
                        outerRadius={120}
                        paddingAngle={8}
                        dataKey="value"
                        animationBegin={0}
                        animationDuration={1500}
                      >
                        {pieData.map((entry, index) => (
                          <Cell key={`cell-${index}`} fill={entry.color} stroke="none" />
                        ))}
                      </Pie>
                      <Tooltip
                        contentStyle={{
                          backgroundColor: theme === 'dark' ? '#111' : '#fff',
                          border: '1px solid var(--border)',
                          borderRadius: '16px',
                          boxShadow: '0 10px 15px -3px rgb(0 0 0 / 0.1)'
                        }}
                      />
                      <Legend verticalAlign="bottom" height={36} iconType="circle" />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </div>

              {/* Sentiment Summary Bar */}
              <div className="bg-card border border-border p-6 md:p-8 rounded-3xl shadow-sm">
                <div className="flex items-center gap-2 mb-8">
                  <TrendingUp className="w-5 h-5 text-primary" />
                  <h3 className="font-bold text-lg">Sentiment Scale</h3>
                </div>
                <div className="h-[280px] md:h-[350px]">
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={barData} layout="vertical" margin={{ top: 5, right: 30, left: 40, bottom: 5 }}>
                      <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="var(--border)" opacity={0.5} />
                      <XAxis type="number" hide />
                      <YAxis dataKey="name" type="category" stroke="var(--muted-foreground)" fontSize={12} tickLine={false} axisLine={false} />
                      <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ backgroundColor: 'var(--card)', border: '1px solid var(--border)', borderRadius: '12px' }} />
                      <Bar dataKey="value" radius={[0, 12, 12, 0]} barSize={40} animationDuration={1500} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>

            {/* AI Takeaways */}
            <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 md:gap-8">
              <div className="bg-gradient-to-br from-emerald-500/5 to-emerald-500/[0.02] border border-emerald-500/10 p-8 md:p-10 rounded-[2.5rem] relative overflow-hidden group hover:border-emerald-500/20 transition-all duration-500">
                <div className="absolute -right-8 -top-8 w-32 h-32 bg-emerald-500/5 rounded-full blur-3xl group-hover:bg-emerald-500/10 transition-colors" />
                <div className="relative">
                  <div className="flex items-center gap-4 mb-8">
                    <div className="w-12 h-12 rounded-2xl bg-emerald-500 flex items-center justify-center shadow-lg shadow-emerald-500/20">
                      <Lightbulb className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-black text-xl tracking-tight">Positive Insights</h3>
                      <p className="text-[10px] font-black uppercase tracking-[0.2em] text-emerald-500/60">Success Patterns</p>
                    </div>
                  </div>
                  <TakeawayList items={data.takeaways.positive} type="positive" />
                </div>
              </div>

              <div className="bg-gradient-to-br from-rose-500/5 to-rose-500/[0.02] border border-rose-500/10 p-8 md:p-10 rounded-[2.5rem] relative overflow-hidden group hover:border-rose-500/20 transition-all duration-500">
                <div className="absolute -right-8 -top-8 w-32 h-32 bg-rose-500/5 rounded-full blur-3xl group-hover:bg-rose-500/10 transition-colors" />
                <div className="relative">
                  <div className="flex items-center gap-4 mb-8">
                    <div className="w-12 h-12 rounded-2xl bg-rose-500 flex items-center justify-center shadow-lg shadow-rose-500/20">
                      <AlertCircle className="w-6 h-6 text-white" />
                    </div>
                    <div>
                      <h3 className="font-black text-xl tracking-tight">Critical Feedback</h3>
                      <p className="text-[10px] font-black uppercase tracking-[0.2em] text-rose-500/60">Growth Areas</p>
                    </div>
                  </div>
                  <TakeawayList items={data.takeaways.negative} type="negative" />
                </div>
              </div>
            </div>

            {/* Comments List */}
            <div className="bg-card border border-border rounded-3xl p-6 md:p-10 shadow-sm">
              <div className="flex flex-col md:flex-row md:items-center justify-between gap-6 mb-10">
                <div>
                  <h3 className="font-black text-2xl tracking-tight">Analyzed Feedback</h3>
                  <p className="text-muted-foreground text-sm font-medium mt-1">Drill down into specific customer opinions.</p>
                </div>
                <div className="flex bg-muted p-1 md:p-1.5 rounded-2xl w-full md:w-fit overflow-x-auto no-scrollbar">
                  {(['all', 'positive', 'neutral', 'negative'] as const).map(tab => (
                    <button
                      key={tab}
                      onClick={() => { setSelectedTab(tab); setCurrentPage(1); }}
                      className={cn(
                        "flex-1 md:flex-none px-6 py-2.5 rounded-xl text-xs sm:text-sm font-bold transition-all capitalize whitespace-nowrap",
                        selectedTab === tab
                          ? "bg-card text-foreground shadow-lg ring-1 ring-border"
                          : "text-muted-foreground hover:text-foreground hover:bg-card/50"
                      )}
                    >
                      {tab}
                    </button>
                  ))}
                </div>
              </div>

              <div className="space-y-4 mb-10">
                {paginatedComments.length === 0 ? (
                  <div className="text-center py-20 bg-muted/20 rounded-3xl border border-dashed border-border">
                    <Info className="w-10 h-10 text-muted-foreground/30 mx-auto mb-4" />
                    <p className="text-muted-foreground font-bold">No results found for this selection.</p>
                  </div>
                ) : (
                  paginatedComments.map((comment, i) => (
                    <div key={i} className="group bg-muted/10 border border-border hover:border-primary/30 p-6 md:p-8 rounded-3xl transition-all duration-300 hover:shadow-md animate-in fade-in slide-in-from-left-4" style={{ animationDelay: `${i * 100}ms` }}>
                      <div className="flex items-start justify-between gap-6">
                        <div className="flex-1">
                          <div className="flex items-center gap-3 mb-4">
                            <span className={cn(
                              "text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full",
                              comment.sentiment === 'positive' ? "bg-emerald-500/10 text-emerald-500 ring-1 ring-emerald-500/20" :
                                comment.sentiment === 'negative' ? "bg-rose-500/10 text-rose-500 ring-1 ring-rose-500/20" :
                                  "bg-zinc-500/10 text-zinc-500 ring-1 ring-zinc-500/20"
                            )}>
                              {comment.sentiment}
                            </span>
                          </div>
                          <p className="text-foreground text-base md:text-lg leading-relaxed font-medium">
                            <span className="text-primary/40 mr-1 text-2xl font-serif">"</span>
                            {comment.text}
                            <span className="text-primary/40 ml-1 text-2xl font-serif">"</span>
                          </p>
                        </div>
                        <div className={cn(
                          "w-12 h-12 rounded-2xl flex items-center justify-center shrink-0 transition-all duration-500 group-hover:rotate-12",
                          comment.sentiment === 'positive' ? "bg-emerald-500 shadow-lg shadow-emerald-500/20 text-white" :
                            comment.sentiment === 'negative' ? "bg-rose-500 shadow-lg shadow-rose-500/20 text-white" :
                              "bg-zinc-500 shadow-lg shadow-zinc-500/20 text-white"
                        )}>
                          {comment.sentiment === 'positive' ? <ThumbsUp className="w-5 h-5" /> :
                            comment.sentiment === 'negative' ? <ThumbsDown className="w-5 h-5" /> : <Minus className="w-5 h-5" />}
                        </div>
                      </div>
                    </div>
                  ))
                )}
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="flex items-center justify-center gap-2">
                  <button
                    onClick={() => setCurrentPage(p => Math.max(1, p - 1))}
                    disabled={currentPage === 1}
                    className="p-3 border border-border rounded-2xl disabled:opacity-20 hover:bg-secondary transition-all active:scale-90"
                  >
                    <ChevronLeft className="w-5 h-5" />
                  </button>
                  <div className="flex items-center gap-2">
                    {Array.from({ length: totalPages }, (_, i) => i + 1).map(page => {
                      // Show limited pages on mobile
                      if (totalPages > 5 && Math.abs(page - currentPage) > 1 && page !== 1 && page !== totalPages) return null;
                      if (totalPages > 5 && Math.abs(page - currentPage) === 2) return <span key={page} className="text-muted-foreground/30">...</span>;

                      return (
                        <button
                          key={page}
                          onClick={() => setCurrentPage(page)}
                          className={cn(
                            "w-10 h-10 rounded-xl text-sm font-black transition-all active:scale-95",
                            currentPage === page
                              ? "bg-primary text-primary-foreground shadow-lg shadow-primary/20 scale-110"
                              : "hover:bg-secondary text-muted-foreground"
                          )}
                        >
                          {page}
                        </button>
                      );
                    })}
                  </div>
                  <button
                    onClick={() => setCurrentPage(p => Math.min(totalPages, p + 1))}
                    disabled={currentPage === totalPages}
                    className="p-3 border border-border rounded-2xl disabled:opacity-20 hover:bg-secondary transition-all active:scale-90"
                  >
                    <ChevronRight className="w-5 h-5" />
                  </button>
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      {/* Simplified Footer */}
      <footer className="border-t border-border mt-auto py-8 bg-card/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex flex-col items-center gap-4">
          <div className="flex items-center gap-2">
            <MessageSquare className="w-5 h-5 text-primary" />
            <span className="text-xl font-black tracking-tight uppercase">SocialInsight</span>
          </div>
          <p className="text-[10px] text-muted-foreground uppercase font-black tracking-[0.2em] text-center">
            © 2026 SocialInsight Engine • AI-Driven Sentiment Intelligence
          </p>
        </div>
      </footer>
    </div>
  )
}

export default App
