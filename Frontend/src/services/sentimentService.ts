import type { SentimentSummary } from "../types";

export interface Credentials {
  pageId: string
  accessToken: string
  geminiApiKey: string
}

export async function fetchPosts(credentials: Omit<Credentials, 'geminiApiKey'>) {
  const res = await fetch("http://localhost:8000/posts", {
    method: "GET",
    headers: {
      "X-FB-Page-Id": credentials.pageId,
      "X-FB-Access-Token": credentials.accessToken,
    },
  });

  if (!res.ok) {
    throw new Error("Failed to fetch posts. Please check your credentials.");
  }

  return res.json();
}

export async function fetchSentimentByPostId(
  postId: string,
  credentials: Credentials
): Promise<SentimentSummary> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
  };

  if (credentials.pageId) {
    headers["X-FB-Page-Id"] = credentials.pageId;
  }
  if (credentials.accessToken) {
    headers["X-FB-Access-Token"] = credentials.accessToken;
  }

  // 1) Trigger scraping for this post
  const scrapeRes = await fetch("http://localhost:8000/scrape", {
    method: "POST",
    headers,
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
