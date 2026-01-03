import type { SentimentSummary } from "../types";

export async function fetchSentimentByPostId(
  postId: string
): Promise<SentimentSummary> {
  const res = await fetch(`http://localhost:8000/classify?post_id=${postId}`);

  if (!res.ok) {
    throw new Error("Failed to fetch sentiment");
  }

  return res.json();
}
