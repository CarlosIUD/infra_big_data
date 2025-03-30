import pandas as pd
import os

# Define input and output paths
input_csv_path = '/Users/magda/Desktop/infra_big_data/input/investments.csv'
output_json_path = '/Users/magda/Desktop/infra_big_data/output/investments.json'

# Read the CSV file
df = pd.read_csv(input_csv_path)

# Make sure the output directory exists
os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

# Convert and save to JSON
df.to_json(output_json_path, orient='records', lines=True)

print(f"JSON file saved to: {output_json_path}")
