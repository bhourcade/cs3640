import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Read the CSV file (ensure path is correct)
df = pd.read_csv("./data/data_analysis.csv")

# Remove entries with zero Word length or invalid Reading level values
# Just an extra check since dataset may not be perfect
df = df[(df["Word length"] > 0) & (df["Reading level"] < 100)]

# Visualization 1: Number of Universities Including CCPA or CPRA
ccpa_counts = df["CCPA or CPRA"].value_counts()

# Plotting the counts
plt.figure(figsize=(6, 4))
ccpa_counts.plot(kind="bar", color=["salmon", "skyblue"])
plt.title("Number of Universities Including CCPA or CPRA")
plt.xlabel("Includes CCPA or CPRA")
plt.ylabel("Number of Universities")
plt.xticks(ticks=[0, 1], labels=["No", "Yes"], rotation=0)
plt.tight_layout()
plt.savefig("./assets/ccpa_counts.png", bbox_inches="tight")
plt.clf()

# Visualization 2: Number of Universities with DNSMPI Link
dnsm_counts = df["DNSMPI"].value_counts()

# Plotting the counts
plt.figure(figsize=(6, 4))
dnsm_counts.plot(kind="bar", color=["orange", "lightgreen"])
plt.title("Number of Universities with DNSMPI Link")
plt.xlabel("Has DNSMPI Link")
plt.ylabel("Number of Universities")
plt.xticks(ticks=[0, 1], labels=["No", "Yes"], rotation=0)
plt.tight_layout()
plt.savefig("./assets/dnsmpi_counts.png", bbox_inches="tight")
plt.clf()


# Visualization 3: Average Reading Level by Kind of University
avg_reading_level = (
    df.groupby("Kind of university")["Reading level"].mean().reset_index()
)

plt.figure(figsize=(8, 6))
sns.barplot(
    x="Kind of university", y="Reading level", data=avg_reading_level, palette="Set2"
)
plt.title("Average Reading Level by Kind of University")
plt.xlabel("Kind of University")
plt.ylabel("Average Reading Level")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("./assets/average_reading_level_by_kind.png", bbox_inches="tight")
plt.clf()

# Visualization 4: Average Word Length by Kind of University
avg_word_length = df.groupby("Kind of university")["Word length"].mean().reset_index()

plt.figure(figsize=(8, 6))
sns.barplot(
    x="Kind of university", y="Word length", data=avg_word_length, palette="Set3"
)
plt.title("Average Word Length by Kind of University")
plt.xlabel("Kind of University")
plt.ylabel("Average Word Length")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("./assets/average_word_length_by_kind.png", bbox_inches="tight")
plt.clf()





# Uncomment below for scatter plot
# Most comment above
# # Load data
# file_path = './data/data_analysis.csv'
# data = pd.read_csv(file_path)

# # Assign colors based on university type
# colors = {'Private For Profit': 'blue', 'Private Non-Profit': 'green', 'Public': 'red'}
# data['Color'] = data['Kind of university'].map(colors)

# # Create scatter plot
# plt.figure(figsize=(12, 6))

# # Plot each university
# for index, row in data.iterrows():# Load data
# file_path = './data/data_analysis.csv'
# data = pd.read_csv(file_path)

# # Assign colors based on university type
# colors = {'Private For Profit': 'blue', 'Private Non-Profit': 'green', 'Public': 'red'}
# data['Color'] = data['Kind of university'].map(colors)

# # Create scatter plot
# plt.figure(figsize=(12, 6))

# # Plot each university
# for index, row in data.iterrows():
#     plt.scatter(
#         index,  # X-axis is the index of the university
#         row['Reading level'],  # Y-axis is the reading level
#         color=row['Color'], 
#         label=row['Kind of university'] if row['Kind of university'] not in plt.gca().get_legend_handles_labels()[1] else "",
#         edgecolor='black', alpha=0.8, s=50
#     )

# # Add labels, legend, and title
# plt.title('Scatter Plot of Reading Level by University Index', fontsize=14)
# plt.xlabel('University Index', fontsize=12)
# plt.ylabel('Reading Level', fontsize=12)
# plt.legend(title="University Type", loc='upper right')
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.tight_layout()

# # Save the plot
# plt.savefig('./assets/reading_level_scatter_plot_simple.png')
# plt.close()

# print("Scatter plot saved as './assets/reading_level_scatter_plot_simple.png'.")

#     plt.scatter(
#         index,  # X-axis is the index of the university
#         row['Reading level'],  # Y-axis is the reading level
#         color=row['Color'], 
#         label=row['Kind of university'] if row['Kind of university'] not in plt.gca().get_legend_handles_labels()[1] else "",
#         edgecolor='black', alpha=0.8, s=50
#     )

# # Add labels, legend, and title
# plt.title('Scatter Plot of Reading Level by University Index', fontsize=14)
# plt.xlabel('University Index', fontsize=12)
# plt.ylabel('Reading Level', fontsize=12)
# plt.legend(title="University Type", loc='upper right')
# plt.grid(True, linestyle='--', alpha=0.6)
# plt.tight_layout()

# # Save the plot
# plt.savefig('./assets/reading_level_scatter_plot_simple.png')
# plt.close()

# print("Scatter plot saved as './assets/reading_level_scatter_plot_simple.png'.")
