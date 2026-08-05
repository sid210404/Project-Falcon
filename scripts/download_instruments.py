from pathlib import Path
import pandas as pd

from app.broker.kite_client import KiteBroker

# Initialize broker
broker = KiteBroker()

print("Downloading instruments...")

# Fetch all NSE instruments
instruments = broker.kite.instruments("NSE")

# Convert to DataFrame
df = pd.DataFrame(instruments)

# Create data directory if it doesn't exist
data_dir = Path("data")
data_dir.mkdir(exist_ok=True)

# Save CSV
output_file = data_dir / "instruments.csv"
df.to_csv(output_file, index=False)

print(f"Downloaded {len(df)} NSE instruments.")
print(f"Saved to: {output_file.resolve()}")

# Preview
print("\nFirst 10 instruments:")
print(df[["tradingsymbol", "instrument_token", "exchange", "segment"]].head(10))