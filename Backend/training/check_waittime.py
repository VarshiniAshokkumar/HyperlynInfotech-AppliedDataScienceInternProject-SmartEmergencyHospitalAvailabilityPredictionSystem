import pandas as pd

df = pd.read_csv(
    "../datasets/er_wait_time/ER Wait Time Dataset.csv"
)

print("\nCOLUMNS:\n")
print(df.columns)

print("\nFIRST 5 ROWS:\n")
print(df.head())