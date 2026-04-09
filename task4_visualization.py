import pandas as pd
import matplotlib.pyplot as plt
import os


# ---------------------------
# Load data
# ---------------------------
def load_data():
    """
    Loads analysed CSV file into DataFrame.
    """
    df = pd.read_csv("data/trends_analysed.csv")
    return df


# ---------------------------
# Create output folder
# ---------------------------
def setup_output():
    """
    Creates outputs/ folder if not exists.
    """
    os.makedirs("outputs", exist_ok=True)


# ---------------------------
# Shorten long titles
# ---------------------------
def shorten_title(title, max_len=50):
    """
    Shortens titles longer than max_len characters.
    """
    return title if len(title) <= max_len else title[:47] + "..."


# ---------------------------
# Chart 1: Top 10 stories
# ---------------------------
def chart_top_stories(df):
    """
    Horizontal bar chart of top 10 stories by score.
    """
    top10 = df.sort_values(by="score", ascending=False).head(10)

    titles = [shorten_title(t) for t in top10["title"]]

    plt.figure()
    plt.barh(titles, top10["score"])
    plt.xlabel("Score")
    plt.ylabel("Story Title")
    plt.title("Top 10 Stories by Score")
    plt.gca().invert_yaxis()

    plt.savefig("outputs/chart1_top_stories.png")
    plt.close()


# ---------------------------
# Chart 2: Stories per category
# ---------------------------
def chart_categories(df):
    """
    Bar chart showing number of stories per category.
    """
    counts = df["category"].value_counts()

    plt.figure()
    plt.bar(counts.index, counts.values)
    plt.xlabel("Category")
    plt.ylabel("Number of Stories")
    plt.title("Stories per Category")

    plt.savefig("outputs/chart2_categories.png")
    plt.close()


# ---------------------------
# Chart 3: Scatter plot
# ---------------------------
def chart_scatter(df):
    """
    Scatter plot of score vs comments.
    Different colors for popular vs non-popular.
    """
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]

    plt.figure()
    plt.scatter(popular["score"], popular["num_comments"], label="Popular")
    plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

    plt.xlabel("Score")
    plt.ylabel("Number of Comments")
    plt.title("Score vs Comments")
    plt.legend()

    plt.savefig("outputs/chart3_scatter.png")
    plt.close()


# ---------------------------
# Dashboard (Bonus)
# ---------------------------
def create_dashboard(df):
    """
    Combines all charts into one figure.
    """
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Top stories
    top10 = df.sort_values(by="score", ascending=False).head(10)
    titles = [shorten_title(t) for t in top10["title"]]
    axes[0].barh(titles, top10["score"])
    axes[0].set_title("Top Stories")
    axes[0].invert_yaxis()

    # Categories
    counts = df["category"].value_counts()
    axes[1].bar(counts.index, counts.values)
    axes[1].set_title("Categories")

    # Scatter
    popular = df[df["is_popular"] == True]
    not_popular = df[df["is_popular"] == False]
    axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
    axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
    axes[2].set_title("Score vs Comments")
    axes[2].legend()

    fig.suptitle("TrendPulse Dashboard")

    plt.savefig("outputs/dashboard.png")
    plt.close()


# ---------------------------
# Main
# ---------------------------
def main():
    setup_output()
    df = load_data()

    chart_top_stories(df)
    chart_categories(df)
    chart_scatter(df)
    create_dashboard(df)

    print("All charts saved in outputs/ folder")


# ---------------------------
# Run
# ---------------------------
if __name__ == "__main__":
    main()
    