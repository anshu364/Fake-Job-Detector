import pandas as pd

# Load dataset
df = pd.read_csv("data/fake_job_postings.csv")

# Combine important text columns
text_columns = [
    "title",
    "company_profile",
    "description",
    "requirements",
    "benefits"
]

# Replace missing values with empty text
for column in text_columns:
    df[column] = df[column].fillna("")

# Create one combined text column
df["combined_text"] = df[text_columns].agg(" ".join, axis=1)

# Keep only useful columns
clean_df = df[["combined_text", "fraudulent"]]

# Remove empty text rows
clean_df = clean_df[clean_df["combined_text"].str.strip() != ""]

print("Original dataset:", df.shape)
print("Clean dataset:", clean_df.shape)

print("\nMissing values:")
print(clean_df.isnull().sum())

print("\nFraudulent vs Legitimate:")
print(clean_df["fraudulent"].value_counts())

# Save cleaned dataset
clean_df.to_csv("data/cleaned_jobs.csv", index=False)

print("\nCleaned dataset saved successfully!")