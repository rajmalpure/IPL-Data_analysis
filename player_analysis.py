import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
df = pd.read_csv("deliveries.csv")

# Check column names
print("Columns in the dataset:", df.columns.tolist())

# Filter legal deliveries (exclude wides and no-balls using 'extras_type')
if 'extras_type' in df.columns:
    legal_balls = df[~df['extras_type'].isin(['wides', 'no_ball'])]
else:
    legal_balls = df.copy()

# Total runs per batter
runs = df.groupby("batter")["batsman_runs"].sum().sort_values(ascending=False)

# Balls faced (only legal deliveries)
balls_faced = legal_balls.groupby("batter").size()

# Number of 4s and 6s
fours = df[df["batsman_runs"] == 4].groupby("batter").size()
sixes = df[df["batsman_runs"] == 6].groupby("batter").size()

# Combine all stats into one DataFrame
batsman_df = pd.DataFrame({
    "Runs": runs,
    "Balls": balls_faced,
    "4s": fours,
    "6s": sixes
}).fillna(0)

# Convert numeric values to integers
batsman_df = batsman_df.astype({"Runs": int, "Balls": int, "4s": int, "6s": int})

# Add batter as index name (important for plotting)
batsman_df.index.name = "batter"

# Top 25 run scorers
batsman_df_top_25 = batsman_df.sort_values(by="Runs", ascending=False).head(25)

# Print top 25 run scorers
print("\nTop 25 Run Scorers in IPL:")
print(batsman_df_top_25)

# Visualization for Top 25 Batsmen (Runs)
plt.figure(figsize=(12, 6))
sns.barplot(data=batsman_df_top_25.reset_index(), x="batter", y="Runs", palette="magma")
plt.title("Top 25 Run Scorers in IPL")
plt.xlabel("Batsman")
plt.ylabel("Total Runs")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
