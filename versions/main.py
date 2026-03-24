
from flask import Flask, render_template_string, request

app = Flask(__name__)

# This is your HTML/CSS template stored as a string
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hands On | Volunteer Finder</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background-color: #f4f7f6; margin: 0; display: flex; flex-direction: column; align-items: center; }
        header { background: #2c3e50; color: white; width: 100%; padding: 1rem 0; text-align: center; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .container { max-width: 800px; width: 90%; margin: 2rem auto; background: white; padding: 2rem; border-radius: 8px; box-shadow: 0 4px 15px rgba(0,0,0,0.05); }
        .search-box { display: flex; gap: 10px; margin-bottom: 2rem; }
        input[type="text"] { flex-grow: 1; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 16px; }
        button { padding: 12px 24px; background: #27ae60; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #219150; }
        .result-card { border-left: 5px solid #27ae60; background: #fafafa; padding: 15px; margin-bottom: 15px; border-radius: 4px; }
        .result-card h3 { margin-top: 0; color: #2c3e50; }
        .tag { display: inline-block; background: #e8f5e9; color: #2e7d32; padding: 4px 8px; border-radius: 4px; font-size: 12px; font-weight: bold; }
    </style>
</head>
<body>
    <header>
        <h1>Hands On 🤝</h1>
        <p>AI-Powered Volunteer Opportunity Aggregator</p>
    </header>

    <div class="container">
        <form method="POST" class="search-box">
            <input type="text" name="location" placeholder="Enter your city (e.g., New York, Austin)..." required>
            <button type="submit">Find Opportunities</button>
        </form>

        {% if results %}
            <h2>Opportunities in {{ location }}</h2>
            {% for item in results %}
                <div class="result-card">
                    <span class="tag">{{ item.type }}</span>
                    <h3>{{ item.title }}</h3>
                    <p><strong>Organization:</strong> {{ item.org }}</p>
                    <p>{{ item.desc }}</p>
                </div>
            {% endfor %}
        {% elif searched %}
            <p>No opportunities found for "{{ location }}". Try another city!</p>
        {% endif %}
    </div>
</body>
</html>
"""

def mock_ai_scraper(location):
    """
    In your full project, this function would use BeautifulSoup or 
    an AI API to find real data. For now, it returns mock data.
    """
    database = {
        "new york": [
            {"title": "Central Park Clean-up", "org": "NYC Parks", "type": "Environment", "desc": "Help us keep the lungs of the city green."},
            {"title": "Soup Kitchen Server", "org": "Bowery Mission", "type": "Social Service", "desc": "Assisting in meal preparation and service."}
        ],
        "austin": [
            {"title": "Animal Shelter Volunteer", "org": "Austin Pets Alive", "type": "Animals", "desc": "Dog walking and kitten socialization."},
            {"title": "Tech Mentor", "org": "Code for ATX", "type": "Education", "desc": "Mentor high schoolers in Python basics."}
        ]
    }
    return database.get(location.lower(), [])

@app.route("/", methods=["GET", "POST"])
def main():
    results = []
    location = ""
    searched = False

    if request.method == "POST":
        location = request.form.get("location")
        results = mock_ai_scraper(location)
        searched = True

    return render_template_string(HTML_TEMPLATE, results=results, location=location, searched=searched)

if __name__ == "__main__":
    # Set debug=True to see changes immediately during development
    app.run(debug=True)