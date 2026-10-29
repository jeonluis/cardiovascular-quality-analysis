import csv
import sqlite3

# STEP 1: Read the CSV dataset
with open("data/patients.csv", newline="") as file:
    patients = list(csv.DictReader(file))

print("Patient records loaded:", len(patients))

# STEP 2: Create a temporary SQLite database
conn = sqlite3.connect(":memory:")

conn.execute("""
CREATE TABLE patients (
    patient_id INTEGER,
    age INTEGER,
    procedure TEXT,
    los_days INTEGER,
    readmitted_30d INTEGER
)
""")

# STEP 3: Insert patient records into SQLite
for patient in patients:
    conn.execute(
        "INSERT INTO patients VALUES (?, ?, ?, ?, ?)",
        (
            int(patient["patient_id"]),
            int(patient["age"]),
            patient["procedure"],
            int(patient["los_days"])
            if patient["los_days"] else None,
            int(patient["readmitted_30d"])
        )
    )

# STEP 4: Run a SQL analysis
query = """
SELECT
    procedure,
    COUNT(*) AS total_patients,
    ROUND(AVG(los_days), 2) AS average_los,
    SUM(readmitted_30d) AS readmissions
FROM patients
GROUP BY procedure
ORDER BY procedure
"""

print("\nCARDIOVASCULAR PROCEDURE ANALYSIS")
print("---------------------------------")

for row in conn.execute(query):
    print(row)

# STEP 5: Identify missing clinical data
missing_query = """
SELECT COUNT(*)
FROM patients
WHERE los_days IS NULL
"""

missing = conn.execute(missing_query).fetchone()[0]

print("\nMissing length-of-stay records:", missing)



print("\nCLINICAL DATA VALIDATION")
print("------------------------")

# Check for duplicate patient IDs
duplicates = conn.execute("""
SELECT patient_id, COUNT(*)
FROM patients
GROUP BY patient_id
HAVING COUNT(*) > 1
""").fetchall()

print("Duplicate patient IDs:", duplicates)

# Check for invalid ages
invalid_ages = conn.execute("""
SELECT COUNT(*)
FROM patients
WHERE age < 0 OR age > 120
""").fetchone()[0]

print("Invalid ages:", invalid_ages)

# Check for invalid lengths of stay
invalid_los = conn.execute("""
SELECT COUNT(*)
FROM patients
WHERE los_days < 0
""").fetchone()[0]

print("Invalid LOS values:", invalid_los)

# Check for invalid readmission indicators
invalid_readmissions = conn.execute("""
SELECT COUNT(*)
FROM patients
WHERE readmitted_30d NOT IN (0, 1)
   OR readmitted_30d IS NULL
""").fetchone()[0]

print("Invalid readmission values:", invalid_readmissions)
conn.close()
