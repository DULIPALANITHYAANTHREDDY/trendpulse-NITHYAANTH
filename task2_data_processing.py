import pandas as pd
import json
import os


# ---------------------------
# Load JSON file
# ---------------------------
def load_json():
    """
    Loads the latest JSON file from data/ folder into a DataFrame.
    """
    files = [f for f in os.listdir("data") if f.startswith("trends_") and f.endswith(".json")]

    if not files:
        print("No JSON files found!")
        return None

    latest_file = sorted(files)[-1]
    filepath = os.path.join("data", latest_file)

    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    print(f"Loaded {len(df)} stories from {filepath}")
    return df


# ---------------------------
# Clean Data
# ---------------------------
def clean_data(df):
    """
    Cleans dataset step-by-step and prints row counts after each step.
    """

    # Remove duplicates
    before = len(df)
    df = df.drop_duplicates(subset="post_id")
    print(f"After removing duplicates: {len(df)}")

    # Remove missing critical fields
    df = df.dropna(subset=["post_id", "title", "score"])
    print(f"After removing nulls: {len(df)}")

    # Fix data types
    df["score"] = pd.to_numeric(df["score"], errors="coerce")
    df["num_comments"] = pd.to_numeric(df["num_comments"], errors="coerce").fillna(0)

    df["score"] = df["score"].astype(int)
    df["num_comments"] = df["num_comments"].astype(int)

    # Remove low-quality stories
    df = df[df["score"] >= 5]
    print(f"After removing low scores: {len(df)}")

    # Clean whitespace in title
    df["title"] = df["title"].str.strip()

    return df


# ---------------------------
# Save CSV
# ---------------------------
def save_csv(df):
    """
    Saves cleaned DataFrame to CSV and prints summary.
    """
    os.makedirs("data", exist_ok=True)

    filepath = "data/trends_clean.csv"
    df.to_csv(filepath, index=False)

    print(f"\nSaved {len(df)} rows to {filepath}")

    # Category summary
    print("\nStories per category:")
    print(df["category"].value_counts())


# ---------------------------
# Main
# ---------------------------
def main():
    df = load_json()

    if df is None:
        return

    df = clean_data(df)
    save_csv(df)


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    main()