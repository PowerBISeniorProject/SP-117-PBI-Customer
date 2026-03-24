import pandas as pd

# Config

INPUT_FILE  = "data/raw/amazon.csv"     
OUTPUT_FILE = "data/processed/amazon.csv" 
INR_TO_USD  = 84.0 # Currency conversion rate 

# Load Raw Data

print("Loading raw data...")
df = pd.read_csv(INPUT_FILE)
print(f"  Rows loaded: {len(df)}")
print(f"  Columns:     {list(df.columns)}\n")

# Fix Price Columns

print("Cleaning price columns...")
df['discounted_price'] = (
    df['discounted_price']
    .str.replace('₹', '', regex=False)
    .str.replace(',', '', regex=False)
    .astype(float)
)
df['actual_price'] = (
    df['actual_price']
    .str.replace('₹', '', regex=False)
    .str.replace(',', '', regex=False)
    .astype(float)
)

# Convert to USD and round to 2 decimal places
df['discounted_price_usd'] = (df['discounted_price'] / INR_TO_USD).round(2)
df['actual_price_usd']     = (df['actual_price']     / INR_TO_USD).round(2)
df.drop(columns=['discounted_price', 'actual_price'], inplace=True)
print("  discounted_price_usd and actual_price_usd created.\n")

# Fix Discount Percentage

print("Cleaning discount_percentage...")
df['discount_percentage'] = (
    df['discount_percentage']
    .str.replace('%', '', regex=False)
    .astype(float)
)
print("  discount_percentage is now numeric.\n")

# Fix Rating Count

print("Cleaning rating_count...")
df['rating_count'] = (
    df['rating_count']
    .str.replace(',', '', regex=False)
    .astype(float)         
)
print(f"  rating_count nulls: {df['rating_count'].isna().sum()}\n")

# Fix Rating Column 

print("Cleaning rating column...")
before = len(df)
df['rating'] = pd.to_numeric(df['rating'], errors='coerce') 
df.dropna(subset=['rating'], inplace=True)
dropped = before - len(df)
print(f"  Rows dropped (invalid rating): {dropped}")
print(f"  Rating range: {df['rating'].min()} – {df['rating'].max()}\n")

# Simplify Categories

print("Simplifying category column...")
df['category'] = df['category'].str.split('|').str[0]
print(f"  Unique categories after simplification: {df['category'].nunique()}\n")

# Drop Unused Columns

print("Dropping unused columns...")
cols_to_drop = [
    'img_link',       
    'product_link',  
    'user_id',       
    'review_id',     
    'about_product',  
]
df.drop(columns=cols_to_drop, inplace=True)
print(f"  Columns remaining: {list(df.columns)}\n")

# Final Column Order & Data Types Summary

FINAL_COLUMNS = [
    'product_id',
    'product_name',
    'category',
    'discounted_price_usd',
    'actual_price_usd',
    'discount_percentage',
    'rating',
    'rating_count',
    'user_name',
    'review_title',
    'review_content',
]

df = df[FINAL_COLUMNS]

print("Final data types:")
print(df.dtypes.to_string())
print(f"\nFinal shape: {df.shape[0]} rows × {df.shape[1]} columns\n")

# Save Cleaned CSV 

df.to_csv(OUTPUT_FILE, index=False)
print(f"✓ Cleaned file saved to: {OUTPUT_FILE}")