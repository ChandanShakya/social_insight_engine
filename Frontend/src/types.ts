export interface SentimentSummary {
  postId: string;
  total: number;
  counts: {
    positive: number;
    neutral: number;
    negative: number;
  };
  percentages: {
    positive: number;
    neutral: number;
    negative: number;
  };
  comments: {
    positive: string[];
    neutral: string[];
    negative: string[];
  };
}
