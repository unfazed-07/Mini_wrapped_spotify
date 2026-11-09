# 🎧 Spotify Mini-Wrapped & AI Taste Analyzer

A lightweight web app that provides on-demand Spotify listening stats, generates an AI-powered taste roast, and curates a customized playlist directly into your Spotify account.

🌐 **Live Demo:** [miniwrappedspotify.streamlit.app](https://miniwrappedspotify.streamlit.app/)

---

## ✨ Features

- **Spotify OAuth Login:** Securely connects to your personal Spotify account.
- **On-Demand Listening Stats:** View your top tracks, artists, and genre breakdown across 3 timeframes (4 weeks, 6 months, and all-time).
- **AI Music Taste Roast:** Leverages an LLM to generate a witty critique and personality analysis based on your listening habits.
- **1-Click Playlist Creation:** Automatically compiles tailored song recommendations and saves them as a new playlist directly to your Spotify library.

---

## 🛠️ Tech Stack

- **Frontend & App Framework:** [Streamlit](https://streamlit.io/)
- **Spotify Integration:** [Spotipy](https://spotipy.readthedocs.io/) (Spotify Web API)
- **AI Analysis:** Google Gemini API / Groq API
- **Data & Config:** `pandas`, `python-dotenv`

---

## 🚀 Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/unfazed-07/Mini_wrapped_spotify.git
   cd Mini_wrapped_spotify
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   Create a `.env` file in the root directory:
   ```env
   SPOTIPY_CLIENT_ID="your_spotify_client_id"
   SPOTIPY_CLIENT_SECRET="your_spotify_client_secret"
   SPOTIPY_REDIRECT_URI="http://localhost:8501"
   GEMINI_API_KEY="your_gemini_api_key"
   ```

5. **Run the application:**
   ```bash
   streamlit run app.py
   ```

---

## 📄 License

This project is licensed under the MIT License.