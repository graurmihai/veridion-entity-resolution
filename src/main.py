"""
Project: Veridion Entity Resolution Challenge
Author: Mihai Graur
Description: Main script that loads the dataset, applies entity resolution logic,
             and outputs grouped company records based on similarity.
"""

import sys
# Prevent Python from creating .pyc files
sys.dont_write_bytecode = True

import pandas as pd
import compare_companies

# Number of rows to process for testing/performance (set to None to process all)
MAX_ROWS_TO_PROCESS = 1000

# Load the dataset from a .parquet file
print("Loading dataset...")
df = pd.read_parquet("data/veridion_entity_resolution_challenge.snappy.parquet")

# If set to None, the entire dataset will be used
if MAX_ROWS_TO_PROCESS is not None:
    df = df.head(MAX_ROWS_TO_PROCESS)
    print(f"Loaded {len(df)} rows (limited by MAX_ROWS_TO_PROCESS).")
else:
    print(f"Loaded entire dataset with {len(df)} rows.")

# Identifier for each group of duplicates
group_id = 0
# Set to keep track of already processed indices
used = set()
# Final list of rows with assigned group IDs
results = []

print("Starting duplicate detection...")

# Compare every row with the remaining ones to find duplicates
# Loop through all rows in the DataFrame
for i in range(len(df)):
    # Skip rows that have already been assigned to a group
    if i in used:
        continue

    # Start a new group with a unique group_id
    group_id += 1
    row_i = df.iloc[i]
    group = [i]  # Initialize group with the current index

    # Compare current row to all following rows
    for j in range(i + 1, len(df)):
        # Skip rows already matched to a previous group
        if j in used:
            continue
        row_j = df.iloc[j]

        # Use the enhanced comparison logic to determine duplicates
        if compare_companies.is_duplicate_enhanced(row_i, row_j):
            # Add to group if duplicate
            group.append(j)
            # Mark this index as processed
            used.add(j)

    # Record group results with group_id and original index
    for idx in group:
        row_data = df.iloc[idx].to_dict()
        row_data["group_id"] = group_id
        row_data["original_index"] = idx
        results.append(row_data)

print(f"Detected {group_id} groups of potential duplicates.")

# Convert the grouped results back to a DataFrame
out_df = pd.DataFrame(results)

print("Saving grouped results to output/grouped_results.csv...")

# Output the result in the "output" folder
out_df.to_csv("output/grouped_results.csv", index=False)

print("Done.")
