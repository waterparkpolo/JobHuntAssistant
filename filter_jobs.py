import re
import pandas as pd

def load_keywords(file_path="config/keywords.txt"):
    with open(file_path, "r") as f:
        return [line.strip().lower() for line in f.readlines() if line.strip()]

def contains_keyword(text, keyword):
    return re.search(r"\b" + re.escape(keyword) + r"\b", text) is not None

def rank_jobs(csv_file="data/all_jobs.csv", output_file="data/ranked_jobs.csv",
              keywords_file="config/keywords.txt", exclude_file="config/exclude_keywords.txt"):
    df = pd.read_csv(csv_file)
    keywords = load_keywords(keywords_file)
    exclude_keywords = load_keywords(exclude_file)

    titles = df["title"].astype(str).str.lower()

    is_senior = titles.apply(lambda t: any(contains_keyword(t, kw) for kw in exclude_keywords))
    excluded_count = int(is_senior.sum())
    df = df[~is_senior]

    scores = titles[~is_senior].apply(lambda t: sum(1 for kw in keywords if contains_keyword(t, kw)))
    df["score"] = scores

    df_sorted = df.sort_values(by="score", ascending=False)
    df_sorted.to_csv(output_file, index=False)
    print(f"✅ Ranked jobs saved to {output_file} ({excluded_count} senior/lead postings filtered out)")

if __name__ == "__main__":
    rank_jobs()
