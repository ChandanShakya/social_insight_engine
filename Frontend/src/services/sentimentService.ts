import type { SentimentSummary } from "../types";

export async function fetchSentimentByPostId(
  postId: string
): Promise<SentimentSummary> {
  // 1) Trigger scraping for this post
  const scrapeRes = await fetch("http://localhost:8000/scrape", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ post_id: postId }),
  });

  if (!scrapeRes.ok) {
    throw new Error("Failed to scrape comments for this post");
  }

  // 2) After scraping completes, fetch classification
  const res = await fetch(`http://localhost:8000/classify?post_id=${encodeURIComponent(postId)}`);

  if (!res.ok) {
    throw new Error("Failed to fetch sentiment");
  }

  return res.json();
}
