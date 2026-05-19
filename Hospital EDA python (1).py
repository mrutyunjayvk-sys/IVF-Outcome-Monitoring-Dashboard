import pandas as pd
from scipy.stats import skew, kurtosis

# Load Excel
df = pd.read_excel("D:\Project 2\Garbha Analytics-Data Driven IVF Outcome Monitoring-309\Data\Reports and Dashboards Data3.xlsx", sheet_name=0)

# Clean column names
df.columns = df.columns.str.strip().str.replace("\n", " ").str.replace("?", "", regex=False)

# Find column(s) containing "embryo" and "transfer" safely
embryo_cols = [str(c) for c in df.columns if "embryo" in str(c).lower() and "transfer" in str(c).lower()]
print("Embryo transfer columns found:", embryo_cols)

eda_cols = [
    "Age (In Years)",
    "Body Mass Index (BMI)",
    "Serum FSH value (In IU/L)",
    "Serum AMH value (In pmol/L)",
    "Value of antral follicle count",
    "Serum estradiol value (in pmol/L)",
    "Post ovulatory thickness of the endometrium on day of HCG",
    "Number of oocytes retrieved"
] + embryo_cols

# Keep only existing columns in the dataframe
eda_cols = [col for col in eda_cols if col in df.columns]
print("Final numeric columns for EDA:", eda_cols)


print(df[eda_cols].dtypes)
for col in eda_cols:
    # Convert to numeric, coerce errors to NaN
    df[col] = pd.to_numeric(df[col], errors='coerce')

# Now compute moments safely
from scipy.stats import skew, kurtosis

eda_summary = pd.DataFrame({
    "Mean (1st Moment)": df[eda_cols].mean(),
    "Variance (2nd Moment)": df[eda_cols].var(),
    "Standard Deviation": df[eda_cols].std(),
    "Skewness (3rd Moment)": df[eda_cols].apply(skew, nan_policy='omit'),
    "Kurtosis (4th Moment)": df[eda_cols].apply(kurtosis, nan_policy='omit')
})

eda_summary

import matplotlib.pyplot as plt
import seaborn as sns
#Histogram
for col in eda_cols:
    plt.figure(figsize=(6,4))
    sns.histplot(df[col], kde=True, bins=20)
    plt.title(f"Histogram of {col}")
    plt.show()


#Boxplot
for col in eda_cols:
    plt.figure(figsize=(6,4))
    sns.boxplot(x=df[col])
    plt.title(f"Boxplot of {col}")
    plt.show()
    

#Scatter Plot (2 Continuous Columns)
# Example: Age vs AMH
plt.figure(figsize=(6,4))
sns.scatterplot(x=df["Age (In Years)"], y=df["Serum AMH value (In pmol/L)"])
plt.title("Scatter plot: Age vs AMH")
plt.xlabel("Age (Years)")
plt.ylabel("AMH (pmol/L)")
plt.show()

# Example: BMI vs Number of oocytes retrieved
plt.figure(figsize=(6,4))
sns.scatterplot(x=df["Body Mass Index (BMI)"], y=df["Number of oocytes retrieved"])
plt.title("Scatter plot: BMI vs Oocytes retrieved")
plt.xlabel("BMI")
plt.ylabel("Oocytes retrieved")
plt.show()

#Multivariate Analysis – Correlation Heatmap
plt.figure(figsize=(10,8))
corr_matrix = df[eda_cols].corr()
sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap of Numeric IVF Variables")
plt.show()
