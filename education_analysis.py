import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import numpy as np

# Set style for better visualization
plt.style.use('seaborn-v0_8-darkgrid')

# Set font size for better readability
plt.rcParams.update({'font.size': 10})

# Read the Excel file
df = pd.read_excel('Urban.xlsx', sheet_name='Children_Parents_matched_June24')

# Select required columns
columns = [
    'Login',
    'sex',
    'age',
    'grade',
    "What is your parents' education? Please indicate your mother's or stepmother's education: (Single choice)",
    'Mathematics or algebra',
    'Russian language',
    'Foreign language (primary)'
]

# Create a shorter name for parent education column
df = df[columns].copy()
df = df.rename(columns={
    "What is your parents' education? Please indicate your mother's or stepmother's education: (Single choice)": 'parent_education'
})

# Drop rows with missing values in grades or parental education
df = df.dropna(subset=['parent_education', 'Mathematics or algebra', 'Russian language', 'Foreign language (primary)'])

# Calculate mean grades for each parental education group
subjects = ['Mathematics or algebra', 'Russian language', 'Foreign language (primary)']
mean_grades = df.groupby('parent_education')[subjects].mean()

# Create a bar plot
plt.figure(figsize=(12, 6))
x = range(len(mean_grades.index))
width = 0.25

for i, subject in enumerate(subjects):
    plt.bar([xi + width*i for xi in x], mean_grades[subject], width, label=subject)

plt.xlabel("Parent's Education Level")
plt.ylabel('Average Grade')
plt.title('Student Performance by Parental Education Level')
plt.xticks([xi + width for xi in x], mean_grades.index, rotation=45, ha='right')
plt.legend()
plt.tight_layout()

# Save the plot
plt.savefig('education_analysis.png')

# Create detailed statistical analysis
print("\nDetailed Statistical Analysis:")
print("-" * 50)

# Calculate descriptive statistics for each subject by parent education
for subject in subjects:
    print(f"\n{subject} Analysis:")
    print("-" * 30)
    
    # Basic statistics
    stats_by_group = df.groupby('parent_education')[subject].agg(['mean', 'std', 'count']).round(2)
    print("\nDescriptive Statistics:")
    print(stats_by_group)
    
    # Perform one-way ANOVA
    groups = [group for _, group in df.groupby('parent_education')[subject]]
    f_stat, p_value = stats.f_oneway(*groups)
    print(f"\nOne-way ANOVA:")
    print(f"F-statistic: {f_stat:.2f}")
    print(f"p-value: {p_value:.4f}")

# Overall analysis
print("\nOverall Performance Analysis:")
print("-" * 50)

# Calculate overall means and find best performing group
overall_means = mean_grades.mean(axis=1)
best_group = overall_means.idxmax()
print(f"\nBest performing group: {best_group}")
print(f"Average grades across all subjects:")
print(overall_means.round(2))

# Calculate and display grade differences
grade_range = overall_means.max() - overall_means.min()
print(f"\nGrade gap (highest vs lowest): {grade_range:.2f} points")

# Create additional visualizations
# 1. Box plots for grade distribution
plt.figure(figsize=(15, 6))
plt.subplot(1, 2, 1)
sns.boxplot(data=df.melt(id_vars=['parent_education'], 
                        value_vars=subjects, 
                        var_name='Subject', 
                        value_name='Grade'),
            x='Grade', y='parent_education')
plt.title('Grade Distribution by Parental Education')
plt.tight_layout()

# Save the new plot
plt.savefig('education_analysis_detailed.png')

# Calculate correlation ratio (eta squared)
def correlation_ratio(x, y):
    categories = np.unique(x)
    n = len(x)
    weighted_mean_y = np.average(y)
    categorical_means = np.array([np.average(y[x == category]) for category in categories])
    ss_total = np.sum((y - weighted_mean_y) ** 2)
    ss_between = np.sum(np.fromiter(
        ((np.sum(x == category) * (categorical_mean - weighted_mean_y) ** 2)
         for category, categorical_mean in zip(categories, categorical_means)),
        dtype=float
    ))
    return ss_between / ss_total if ss_total != 0 else 0

# Calculate and print correlation ratios
print("\nCorrelation Analysis:")
print("-" * 50)
for subject in subjects:
    correlation = correlation_ratio(df['parent_education'], df[subject])
    print(f"\nCorrelation ratio (eta-squared) for {subject}: {correlation:.3f}")
    print(f"This suggests that {(correlation * 100):.1f}% of the variance in {subject} ")
    print(f"grades can be explained by parental education level.")
