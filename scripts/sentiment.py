import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

df = pd.read_csv("data/processed/amazon.csv", on_bad_lines="skip")
analyzer = SentimentIntensityAnalyzer()

def get_sentiment_score(text):
    if not isinstance(text, str):
        return 0.0 
    return analyzer.polarity_scores(text)["compound"]

def score_to_label(score):
    if score >= 0.05:
        return "Positive"
    elif score <= -0.05:
        return "Negative"
    else:
        return "Neutral"

# Score both fields
df["title_score"]   = df["review_title"].apply(get_sentiment_score)
df["content_score"] = df["review_content"].apply(get_sentiment_score)

# Combine: average the two scores, then label
df["compound_score"] = (df["title_score"] + df["content_score"]) / 2
df["sentiment"]      = df["compound_score"].apply(score_to_label)

df.to_csv("data/processed/amazon.csv", index=False)
print("Done — sentiment labels added.")
print(df["sentiment"].value_counts())