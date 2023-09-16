import re

text = """   Centennial Carillon Tower
   Centennial Court
   Government & Belleville Streets
   Victoria, British Columbia, Canada
   LL: N 48.42040, W 123.36821"""

# Regular Expression to find latitude and longitude
pattern = r"LL: N (\d+\.\d+), W (\d+\.\d+)"

match = re.search(pattern, text)

if match:
    latitude = float(match.group(1))
    longitude = -float(match.group(2))  # Making it negative because it's 'W'
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Latitude and Longitude not found.")
