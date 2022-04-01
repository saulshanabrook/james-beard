import pandas

df = pandas.read_csv("winners.csv")

no_duplicates = df.drop_duplicates(subset=['place', 'location'])

no_duplicates[:2000].to_csv("place_1.csv", index=False)
no_duplicates[2000:].to_csv("place_2.csv", index=False)