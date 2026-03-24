import requests
from flask import Flask, render_template_string, request

app = Flask(__name__)

# 1. HARDCODE THE KEY HERE FOR THE CAPSTONE (Simplest way to avoid scope issues)
MY_KEY = "9238632307bd01a4b28996b6e1793a3caa42b186198b066c9846e112f4e341f8"

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Hands On | Real-Time Results</title>
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #f4f7f6; padding: 20px; }
        .container { max-width: 800px; margin: auto; background: white; padding: 30px; border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }
        .search-form { display: flex; gap: 10px; margin-bottom: 25px; }
        input { flex: 3; padding: 12px; border: 1px solid #ddd; border-radius: 8px; }
        button { flex: 1; background: #27ae60; color: white; border: none; border-radius: 8px; cursor: pointer; font-weight: bold; }
        .card { border-left: 5px solid #27ae60; padding: 15px; margin-bottom: 15px; background: #fff; border-radius: 4px; box-shadow: 0 2px 5px rgba(0,0,0,0.05); }
        .card a { color: #2c3e50; text-decoration: none; font-size: 1.2rem; font-weight: bold; }
        .card p { color: #666; font-size: 0.9rem; margin: 10px 0; }
        .tag { background: #e8f5e9; color: #2e7d32; padding: 3px 8px; border-radius: 4px; font-size: 0.75rem; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Hands On 🤝</h1>
        <form method="POST" class="search-form">
            <input type="text" name="location" placeholder="e.g. Louisville KY volunteer" required>
            <button type="submit">Search</button>
        </form>

        {% if results %}
            {% for item in results %}
                <div class="card">
                    <span class="tag">Live Opportunity</span><br>
                    <a href="{{ item.link }}" target="_blank">{{ item.title }}</a>
                    <p>{{ item.snippet }}</p>
                </div>
            {% endfor %}
        {% endif %}
    </div>
</body>
</html>
"""

def get_live_data(query):
    # Using the exact same logic as your successful test script
    params = {
        "engine": "google",
        "q": query,
        "api_key": MY_KEY
    }
    try:
        r = requests.get("https://serpapi.com/search", params=params)
        data = r.json()
        # Look for 'organic_results' which contains the actual links
        return data.get("organic_results", [])
    except Exception as e:
        print(f"Error during search: {e}")
        return []

@app.route("/", methods=["GET", "POST"])
def index():
    results = []
    if request.method == "POST":
        user_query = request.form.get("location")
        results = get_live_data(user_query)
    return render_template_string(HTML_TEMPLATE, results=results)

if __name__ == "__main__":
    app.run(debug=True)