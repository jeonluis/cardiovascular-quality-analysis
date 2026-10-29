import csv
from collections import defaultdict
from pathlib import Path
import matplotlib.pyplot as plt

# Load the synthetic cardiovascular dataset
with open("data/patients.csv", newline="") as file:
    patients = list(csv.DictReader(file))

# Group records by procedure
groups = defaultdict(list)

for patient in patients:
    groups[patient["procedure"]].append(patient)

procedures = sorted(groups)

# Calculate quality measures
volumes = []
average_los = []
readmissions = []

for procedure in procedures:
    records = groups[procedure]

    los_values = [
        int(record["los_days"])
        for record in records
        if record["los_days"]
    ]

    volumes.append(len(records))
    average_los.append(
        sum(los_values) / len(los_values)
        if los_values else 0
    )
    readmissions.append(
        sum(int(record["readmitted_30d"])
            for record in records)
    )

# Create output folder
Path("output").mkdir(exist_ok=True)

# Chart 1: Patient volume
plt.figure(figsize=(8, 5))
plt.bar(procedures, volumes)
plt.title("Patient Volume by Procedure")
plt.ylabel("Number of Records")
plt.tight_layout()
plt.savefig("output/patient_volume.png", dpi=150)
plt.close()

# Chart 2: Average length of stay
plt.figure(figsize=(8, 5))
plt.bar(procedures, average_los)
plt.title("Average Length of Stay by Procedure")
plt.ylabel("Days")
plt.tight_layout()
plt.savefig("output/average_los.png", dpi=150)
plt.close()

# Chart 3: Readmissions
plt.figure(figsize=(8, 5))
plt.bar(procedures, readmissions)
plt.title("30-Day Readmissions by Procedure")
plt.ylabel("Number of Readmissions")
plt.tight_layout()
plt.savefig("output/readmissions.png", dpi=150)
plt.close()

print("Dashboard charts created successfully!")
print("Files saved in the output folder.")
