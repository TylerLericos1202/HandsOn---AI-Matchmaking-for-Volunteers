import requests

KEY = "9238632307bd01a4b28996b6e1793a3caa42b186198b066c9846e112f4e341f8"
url = f"https://serpapi.com/search?q=coffee&api_key={KEY}"

response = requests.get(url)
data = response.json()

if "error" in data:
    print(f"❌ Still invalid: {data['error']}")
else:
    print("✅ Success! Your key is working.")
    print(f"First result: {data['organic_results'][0]['title']}")