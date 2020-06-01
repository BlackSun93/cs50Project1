import requests
res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "qjfi7EyD90v3MlEghQNbBQ", "isbns": "9781632168146"})
print(res.json())
