# Educational Achievement Analysis

This project analyzes the relationship between parental education and student academic achievement. The analysis includes statistical testing and visualization of academic performance across different subjects based on parents' educational background.

## Features

- Analysis of three key subjects:
  - Mathematics
  - Russian Language
  - Foreign Language
- Statistical analysis including:
  - One-way ANOVA tests
  - Correlation ratio (eta-squared) calculations
  - Descriptive statistics
- Visualizations:
  - Bar plots of average grades
  - Box plots showing grade distributions

## Requirements

- Python 3.x
- Required packages:
  - pandas
  - matplotlib
  - seaborn
  - scipy
  - numpy

## Installation

```bash
pip install pandas matplotlib seaborn scipy numpy
```

## Usage

1. Place your data file 'Urban.xlsx' in the same directory
2. Run the analysis:
```bash
python education_analysis.py
```

## Output

The script generates two visualization files:
- `education_analysis.png`: Bar plot comparing average grades
- `education_analysis_detailed.png`: Box plots showing grade distributions

## Key Findings

- Students with university-educated parents show highest academic performance
- Statistically significant differences across all subjects (p < 0.001)
- Strongest effect observed in Foreign Language studies
- Parental education explains 3.3-5.5% of grade variance
