# numbers = [2, 4, 6, 8]
# product = 1
#
# for number in numbers:
#     products = product * number
#     print("The product is : ", products)
from requests import get

websites = (
    "google.com",
    "airbnb.com",
    "https://twitter.com",
    "facebook.com",
    "https://tiktok.com"
)

results = {}

for website in websites:
    if not website.startswith("https://"):
        website = f"https://{website}"
    response = get(website)
    if response.status_code == 200:
        results[website] = "OK"
    else:
        results[website] = "FAILED"

print(results)