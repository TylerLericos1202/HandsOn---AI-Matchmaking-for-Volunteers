# 🤝 HandsOn — AI Matchmaking for Volunteers

HandsOn is a web application that connects volunteers with nonprofit opportunities using intelligent matchmaking. Volunteers can create profiles, discover events that align with their skills and interests, and nonprofits can find the right people to make an impact.

---

## ✨ Features

- **AI-Powered Matching** — Intelligently pairs volunteers with opportunities based on their skills, interests, and availability
- **Volunteer Profiles** — Users can create and manage personal profiles highlighting their experience and goals
- **Opportunity Discovery** — Browse and filter volunteer events and nonprofit listings
- **Authentication** — Secure login with Google OAuth
- **Responsive UI** — Clean, accessible interface built with HTML/CSS

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|------------|
| Backend | Python, Flask |
| Frontend | HTML, CSS (Jinja2 templates) |
| Database | SQLite |
| Auth | Google OAuth |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/TylerLericos1202/HandsOn---AI-Matchmaking-for-Volunteers.git
   cd HandsOn---AI-Matchmaking-for-Volunteers
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your_secret_key
   GOOGLE_CLIENT_ID=your_google_client_id
   GOOGLE_CLIENT_SECRET=your_google_client_secret
   ```

5. **Run the app**
   ```bash
   python app.py
   ```

   Visit `http://localhost:5000` in your browser.

---

## 📁 Project Structure

```
handson/
├── app.py                  # Main Flask application
├── instance/
│   └── handson.db          # SQLite database
├── static/
│   ├── style.css           # Global styles
│   └── img/
│       └── favicon.png
├── templates/
│   ├── base.html           # Base layout template
│   ├── index.html          # Home page
│   ├── auth.html           # Login / signup
│   └── profile.html        # User profile page
└── versions/               # Development iterations
```

---

## 🔐 Authentication

HandsOn uses Google OAuth for secure sign-in. To enable it, you'll need to set up a project in the [Google Cloud Console](https://console.cloud.google.com/) and add your credentials to the `.env` file.

---

## 🤝 Contributing

Contributions are welcome! Feel free to open an issue or submit a pull request.

1. Fork the project
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -m 'Add your feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

> Built with ❤️ to make volunteering easier and more impactful.
