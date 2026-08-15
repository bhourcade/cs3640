import pandas as pd
import matplotlib.pyplot as plt

# Load data
file_path = './data/data_analysis.csv'
data = pd.read_csv(file_path)

# Group data by university type
grouped = data.groupby('Kind of university')

# Analysis 1: Averages by university type
averages = grouped[['Word length', 'Reading level', 'Sentiment index']].mean()

# Analysis 2: Privacy standards compliance
compliance = grouped[['CCPA or CPRA', 'FERPA', 'GDPR', 'DNSMPI']].mean()

# Analysis 3: Correlations between metrics
correlations = data[['Word length', 'Reading level', 'Sentiment index']].corr()

# Write results to a text file
output_file = "./data/analysis_results.txt"
with open(output_file, "w") as f:
    f.write("Average Metrics by University Type:\n")
    f.write(averages.to_string())
    f.write("\n\n")

    f.write("Privacy Standards Compliance by University Type (Proportion):\n")
    f.write(compliance.to_string())
    f.write("\n\n")

    f.write("Correlations Between Metrics:\n")
    f.write(correlations.to_string())
    f.write("\n")



# Visualization for clarity

# Bar plot for compliance by university type
compliance.plot(kind='bar', figsize=(10, 6))
plt.title('Privacy Standards Compliance by University Type')
plt.ylabel('Proportion of Compliance')
plt.xlabel('University Type')
plt.xticks(rotation=45)
plt.tight_layout()
# Save chart as image to assets folder. 
# May need to modify the path if throwing an error
plt.savefig('./assets/privacy_compliance_by_university_type.png')  
plt.close()


