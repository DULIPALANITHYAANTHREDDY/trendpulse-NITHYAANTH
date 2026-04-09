import pandas as pd
import numpy as np


# ---------------------------
# Load and explore data
# ---------------------------
def load_data():
    """
    Loads cleaned CSV and prints basic info.
    """
    filepath = "data/trends_clean.csv"

    df = pd.read_csv(filepath)

    print(f"Loaded data: {df.shape}\n")

    print("First 5 rows:")
    print(df.head(), "\n")

    # Average values using Pandas
    avg_score = df["score"].mean()
    avg_comments = df["num_comments"].mean()

    print(f"Average score   : {int(avg_score)}")
    print(f"Average comments: {int(avg_comments)}\n")

    return df, avg_score


# ---------------------------
# NumPy analysis
# ---------------------------
def numpy_analysis(df):
    """
    Performs statistical analysis using NumPy.
    """
    scores = df["score"].values
    comments = df["num_comments"].values

    print("--- NumPy Stats ---")

    print(f"Mean score   : {int(np.mean(scores))}")
    print(f"Median score : {int(np.median(scores))}")
    print(f"Std deviation: {int(np.std(scores))}")

    print(f"Max score    : {int(np.max(scores))}")
    print(f"Min score    : {int(np.min(scores))}\n")

    # Category with most stories
    category_counts = df["category"].value_counts()
    top_category = category_counts.idxmax()
    top_count = category_counts.max()

    print(f"Most stories in: {top_category} ({top_count} stories)\n")

    # Story with most comments
    max_comment_idx = np.argmax(comments)
    top_story = df.iloc[max_comment_idx]

    print(f'Most commented story: "{top_story["title"]}" — {top_story["num_comments"]} comments\n')


# ---------------------------
# Add new columns
# ---------------------------
def add_columns(df, avg_score):
    """
    Adds engagement and popularity metrics.
    """
    # Engagement metric
    df["engagement"] = df["num_comments"] / (df["score"] + 1)

    # Popularity flag
    df["is_popular"] = df["score"] > avg_score

    return df


# ---------------------------
# Save result
# ---------------------------
def save_data(df):
    """
    Saves updated DataFrame to CSV.
    """
    filepath = "data/trends_analysed.csv"
    df.to_csv(filepath, index=False)

    print(f"Saved to {filepath}")


# ---------------------------
# Main pipeline
# ---------------------------
def main():
    df, avg_score = load_data()
    numpy_analysis(df)
    df = add_columns(df, avg_score)
    save_data(df)


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    main()