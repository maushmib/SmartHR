import pandas as pd
import os
import numpy as np

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
csv_path = os.path.join(BASE_DIR, 'attrition_data.csv')
new_csv_path = os.path.join(BASE_DIR, 'attrition_data_engineering.csv')

df = pd.read_csv(csv_path)

# Role mapping
role_mapping = {
    "Sales Executive": "Software Engineer",
    "Research Scientist": "Data Scientist",
    "Laboratory Technician": "QA Engineer",
    "Manufacturing Director": "DevOps Engineer",
    "Healthcare Representative": "Support Engineer",
    "Manager": "Engineering Manager",
    "Human Resources": "HR Manager",
    "Research Director": "Tech Lead",
    "Sales Representative": "Junior Developer"
}
df["JobRole"] = df["JobRole"].map(role_mapping)

# Education mapping
edu_mapping = {
    "Life Sciences": "Computer Science",
    "Medical": "Information Technology",
    "Marketing": "Electronics",
    "Technical Degree": "Mechanical",
    "Other": "Civil",
    "Human Resources": "Business Administration"
}
df["EducationField"] = df["EducationField"].map(edu_mapping)

# Assign realistic salary ranges
salary_ranges = {
    "Junior Developer": (25000, 50000),
    "Software Engineer": (50000, 100000),
    "QA Engineer": (40000, 80000),
    "DevOps Engineer": (70000, 150000),
    "Support Engineer": (30000, 60000),
    "Engineering Manager": (150000, 300000),
    "HR Manager": (60000, 120000),
    "Tech Lead": (120000, 250000),
    "Data Scientist": (80000, 200000),
}

# Replace MonthlyIncome with realistic salaries
df["MonthlyIncome"] = df.apply(
    lambda row: np.random.randint(
        salary_ranges[row["JobRole"]][0], salary_ranges[row["JobRole"]][1]
    ),
    axis=1
)

# Save updated dataset
df.to_csv(new_csv_path, index=False)
print("✅ Engineering HR dataset with realistic salaries created:", new_csv_path)
