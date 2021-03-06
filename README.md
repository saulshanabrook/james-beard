# James Beard Data
Scraped [James Beard Foundationa](https://www.jamesbeard.org/) data.

Uploaded to [Google Maps](https://www.google.com/maps/d/u/0/edit?mid=1TEs9aPQMejGKbP4bPZqlng_Iab29GCbp&usp=sharing).

Requirements:

- [`aiohttp-client-cache`](https://github.com/JWCook/aiohttp-client-cache#aiohttp-client-cache) for cachd requests
- `pandas` for saving/reading to CSV.
- [`beautifulsoup4`](https://beautiful-soup-4.readthedocs.io/en/latest/#) for parsing HTML

Steps:

1. `python main.py` Scrapes all james beard nominees into `winners.csv`.
2. `python transform.py` Groups nominees by name and chooses the first from each column, and splits into two CSVs, `place_[1,2].csv`, so that each has max 2000 rows.
3. Uploads `place_[1,2].csv` to Google Map Maker.
