
import pandas as pd
import re

# Load the original CSV file
file_path = 'path/to/original/csv/file.csv'
df = pd.read_csv(file_path)

# Functions to extract necessary information
def extract_price(row):
    pattern = r'total:([\d.]+)'
    match = re.search(pattern, row)
    return float(match.group(1)) if match else None

def extract_uitsparingen(row):
    pattern = r'Uitsparingen\s*=(Ja|Nee|[0-9]+\s*-\s*€[0-9.]+)'
    match = re.search(pattern, row)
    return match.group(1) if match else None

def filter_combined_cm_value_below_120(row):
    patterns = [
        r'=(\d+)\s*x\s*\d+\s*cm',
        r'Vul de gewenste breedte in\s*\(cm\)=([\d]+)',
        r'meta:Afmeting keukenachterwand\s*=(\d+)\s*x\s*\d+\s*cm'
    ]
    for pattern in patterns:
        match = re.search(pattern, row)
        if match:
            cm_value = int(match.group(1))
            if cm_value < 120:
                return True
    return False

def filter_combined_cm_value_above_or_equal_120(row):
    patterns = [
        r'=(\d+)\s*x\s*\d+\s*cm',
        r'Vul de gewenste breedte in\s*\(cm\)=([\d]+)',
        r'meta:Afmeting keukenachterwand\s*=(\d+)\s*x\s*\d+\s*cm'
    ]
    for pattern in patterns:
        match = re.search(pattern, row)
        if match:
            cm_value = int(match.group(1))
            if cm_value >= 120:
                return True
    return False

# Extract and filter
uitsparingen_column = 'line_items'
df['extracted_price'] = df[uitsparingen_column].apply(lambda x: extract_price(str(x)))
df['extracted_uitsparingen'] = df[uitsparingen_column].apply(lambda x: extract_uitsparingen(str(x)))

df_filtered = df[df['extracted_uitsparingen'].notna() & df[uitsparingen_column].apply(lambda x: not bool(re.search(r'\\|name:Inductie beschermer', str(x))))]

df_uitsparingen_nee_below_120 = df_filtered[(df_filtered['extracted_uitsparingen'] == 'Nee') & df_filtered[uitsparingen_column].apply(lambda x: filter_combined_cm_value_below_120(str(x)))]
df_uitsparingen_nee_above_or_equal_120 = df_filtered[(df_filtered['extracted_uitsparingen'] == 'Nee') & df_filtered[uitsparingen_column].apply(lambda x: filter_combined_cm_value_above_or_equal_120(str(x)))]
df_uitsparingen_ja_or_price_below_120 = df_filtered[(df_filtered['extracted_uitsparingen'] != 'Nee') & df_filtered[uitsparingen_column].apply(lambda x: filter_combined_cm_value_below_120(str(x)))]
df_uitsparingen_ja_or_price_above_or_equal_120 = df_filtered[(df_filtered['extracted_uitsparingen'] != 'Nee') & df_filtered[uitsparingen_column].apply(lambda x: filter_combined_cm_value_above_or_equal_120(str(x)))]

# Save to CSV
df_uitsparingen_nee_below_120.to_csv('emails_uitsparingen_nee_below_120.csv', index=False)
df_uitsparingen_nee_above_or_equal_120.to_csv('emails_uitsparingen_nee_above_or_equal_120.csv', index=False)
df_uitsparingen_ja_or_price_below_120.to_csv('emails_uitsparingen_ja_or_price_below_120.csv', index=False)
df_uitsparingen_ja_or_price_above_or_equal_120.to_csv('emails_uitsparingen_ja_or_price_above_or_equal_120.csv', index=False)
