import pandas as pd

staff = pd.read_csv(
    "../datasets/hospital_beds/staff.csv"
)

schedule = pd.read_csv(
    "../datasets/hospital_beds/staff_schedule.csv"
)

print("\nSTAFF COLUMNS\n")
print(staff.columns)

print("\nSTAFF FIRST 5 ROWS\n")
print(staff.head())

print("\nSCHEDULE COLUMNS\n")
print(schedule.columns)

print("\nSCHEDULE FIRST 5 ROWS\n")
print(schedule.head())