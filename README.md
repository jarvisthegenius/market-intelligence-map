# Market Intelligence Map

Live market intelligence map for Dubai real estate brokers. Displays Sales PSF and Median Annual Rent by area using Property Finder API data.

## Setup

```bash
pip install -r requirements.txt
```

## Usage

```bash
cd src
python generate_market_intelligence.py
```

Output: `market_intelligence.json`

## Data Schema

- `areas`: Array of 30 priority Dubai areas
- `sales`: Median PSF, price, size by bedroom type
- `rent`: Median annual rent by bedroom type (7.5% discount applied)
- `centroid`: Geographic center for map placement
- `listing_counts`: Total buy/rent listings per area