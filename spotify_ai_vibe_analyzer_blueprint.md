# 🎧 Project Blueprint: Personal Spotify "Mini-Wrapped" & AI Playlist Creator

## 1. Project Overview

**What this project does:**
Instead of waiting until December for Spotify Wrapped, this web app lets users **log in with their own Spotify account** anytime to view their personal listening stats, get an AI-generated "Music Taste Roast / Aura Check," and automatically generate & save a personalized playlist directly to their Spotify account!

**Key Practical Features:**
1. **User Login (OAuth 2.0):** Users click "Login with Spotify," authorize the app, and get redirected back seamlessly.
2. **Personal Listening Stats:** Pulls the user's actual Top Tracks, Top Artists, and favorite Genres across 3 time ranges: *Last 4 Weeks*, *Last 6 Months*, or *All-Time*.
3. **Cloud AI "Music Aura & Roast":** Sends the user's top artists and tracks to the **Google Gemini API** to analyze their listening habits, tell them their "music personality," and roast their guilty pleasures.
4. **1-Click Playlist Generator (Actionable Task):** Based on their listening history, the AI curates 10 fresh song recommendations, and the user can click a button to **automatically create and save a new playlist** right into their Spotify library.

---

## 2. Tech Stack & Tools Needed

* **Language:** Python 3.9+
* **Frontend/UI:** [Streamlit](https://streamlit.io/) (Handles the web interface, login buttons, tabs, and charts with pure Python).
* **Spotify Integration:** `spotipy` (Uses `SpotifyOAuth` to handle user logins, tokens, and playlist creation).
* **Cloud AI API:** `google-genai` (Google Gemini API—analyzes listening stats and suggests new tracks in structured JSON).
* **Data Visualization:** `pandas` (Built-in with Streamlit to display neat genre charts and track tables).
* **Environment Management:** `python-dotenv` (Secures your API keys).

---

## 3. Prerequisites (Getting Your API Keys)

### A. Spotify Developer Setup (Crucial for User Login!)
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard) and log in.
2. Click **"Create App"**.
3. Fill in the details:
   * **App name:** `My Mini Wrapped & AI DJ`
   * **App description:** `Personal listening stats and playlist generator`
   * **Redirect URIs:** Enter **`http://localhost:8501`** and click **Add**. *(CRITICAL: This must match your Streamlit local URL so Spotify knows where to send the user after they log in!)*
   * Check the box for **Web API** and click **Save**.
4. Go to **Settings** to copy your **Client ID** and **Client Secret**.
5. *(Note for testing with friends)*: In the dashboard under **User Management**, you can add up to 25 friends' Spotify email addresses so they can log into your app too!

### B. Google Gemini API Key
1. Go to [Google AI Studio](https://aistudio.google.com/).
2. Click **"Get API key"** -> **"Create API key"** and copy it.

---

## 4. Project File Tree

Still super clean—just 4 files in one folder!

```text
spotify-mini-wrapped/
│
├── .env                 # Stores your API keys and Redirect URI
├── requirements.txt     # Python libraries required
├── backend.py           # Handles Spotify OAuth login, fetching user stats, AI calls, & playlist creation
└── app.py               # Streamlit dashboard UI (Login screen, Stats tabs, AI Roast, Playlist button)
```

---

## 5. What Each File Contains

### File 1: `requirements.txt`
```text
streamlit
spotipy
google-genai
python-dotenv
pandas
```

### File 2: `.env`
```env
SPOTIPY_CLIENT_ID="paste_your_spotify_client_id_here"
SPOTIPY_CLIENT_SECRET="paste_your_spotify_client_secret_here"
SPOTIPY_REDIRECT_URI="http://localhost:8501"
GEMINI_API_KEY="paste_your_gemini_api_key_here"
```

### File 3: `backend.py` (Auth, Stats & AI Logic)
This file manages the heavy lifting through 5 clean functions:
1. **`create_spotify_oauth()`**: Configures `SpotifyOAuth` with the required permissions (`scopes`):
   * `user-top-read` (Read user's top artists and tracks)
   * `user-read-recently-played` (Read recently played songs)
   * `playlist-modify-public` & `playlist-modify-private` (Create and add songs to a user's playlist)
2. **`get_user_stats(sp, time_range)`**: Fetches the logged-in user's profile info, Top 10 Tracks, Top 10 Artists, and calculates their top genres for the selected time window (`short_term` = 4 weeks, `medium_term` = 6 months, `long_term` = all time).
3. **`generate_ai_roast_and_recs(top_artists, top_tracks)`**: Sends the user's top music to Gemini API. Returns two things:
   * A fun **Personality Analysis & Friendly Roast** of their music taste.
   * A list of **10 recommended songs** (`Artist - Track Name`) tailored to their taste.
4. **`create_custom_playlist(sp, user_id, playlist_name, recommended_songs)`**: Searches Spotify for each of the 10 recommended songs, creates a brand-new playlist on the user's Spotify account, and adds all the tracks to it!

### File 4: `app.py` (The Streamlit Web App)
Controls the user journey:
* **Step 1 (Login Check):** Checks `st.query_params` to see if Spotify redirected the user back with an authentication `code`. If not logged in, displays a welcoming landing page with a **"🔗 Login with Spotify"** button.
* **Step 2 (Dashboard Header):** Once logged in, greets the user by their Spotify display name and profile picture, and shows a timeframe selector dropdown (*Last 4 Weeks*, *Last 6 Months*, *All Time*).
* **Step 3 (3 Interactive Tabs):**
  * **Tab 1: 📊 My Listening Stats:** Displays Top 10 Tracks (with album art and audio preview links), Top 10 Artists, and a bar chart of their Most Listened Genres.
  * **Tab 2: 🔥 AI Music Aura & Roast:** A button that calls Gemini to judge their music taste, deduce their "listening mood," and rate their mainstream vs. underground score.
  * **Tab 3: 🤖 1-Click AI Playlist Maker:** Displays the 10 AI-recommended songs based on their stats and provides a **"💾 Save Playlist to My Spotify"** button that builds the playlist in their actual Spotify app and gives them a direct link to open it!

---

## 6. Step-by-Step Guide to Build This Using AI

Follow these exact steps and copy-paste the prompts into your AI coding assistant (or ask me right here!) to generate the full working code.

### Step 1: Set Up Your Folder & Environment
Open your terminal and run:
```bash
mkdir spotify-mini-wrapped
cd spotify-mini-wrapped
python -m venv venv
# Activate virtual environment:
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate
```
Create `requirements.txt` and `.env` with your keys, then install:
```bash
pip install -r requirements.txt
```

### Step 2: Prompt AI to Build `backend.py`
Copy and paste this prompt to generate the backend file:

> *"Write a Python file named `backend.py` for a Spotify Mini-Wrapped app. Load environment variables using `python-dotenv`.
> 1. Create `get_oauth()` returning a `spotipy.oauth2.SpotifyOAuth` object using scopes: `'user-top-read user-read-recently-played playlist-modify-public playlist-modify-private'`, with `cache_path=None` so session tokens are handled cleanly in Streamlit.
> 2. Create `get_user_stats(sp, time_range='medium_term')` that takes an authenticated `spotipy.Spotify` client and returns a dictionary with: user profile (display_name, id, image), top 10 tracks (name, artist, album image, spotify url), top 10 artists (name, image, genres, popularity), and a dictionary of top 5 genre counts extracted from their top artists.
> 3. Create `get_ai_analysis_and_recs(top_artists, top_tracks)` using the `google-genai` SDK (`from google import genai`, model `gemini-2.5-flash`). Ask Gemini to return a JSON object with two keys: `'roast_and_aura'` (markdown text giving a playful roast, their music aura/personality, and mainstream score) and `'recommendations'` (a list of 10 strings formatted as `'Track Name - Artist Name'`).
> 4. Create `build_spotify_playlist(sp, user_id, playlist_name, rec_list)` that creates a new public playlist in the user's account, searches Spotify for the first track URI of each string in `rec_list`, adds those tracks to the playlist, and returns the external Spotify URL of the newly created playlist."*

### Step 3: Prompt AI to Build `app.py`
Copy and paste this prompt to generate the Streamlit frontend:

> *"Write a Streamlit app named `app.py` that imports the functions from `backend.py`.
> 1. Handle Spotify OAuth flow cleanly using `st.session_state` and `st.query_params`:
>    - If `'token_info'` is not in `st.session_state`, check if `'code'` is in `st.query_params`. If `'code'` is present, exchange it for a token using `oauth.get_access_token(code)`, store it in `st.session_state['token_info']`, and clear query params.
>    - If still not authenticated, display a centered landing screen with a link button (`st.link_button`) pointing to `oauth.get_authorize_url()` labeled '🎧 Login with Spotify'.
> 2. Once authenticated, initialize `sp = spotipy.Spotify(auth=st.session_state['token_info']['access_token'])`.
> 3. Add a sidebar with the user's Spotify profile name, a selectbox for Time Range ('short_term' as 'Last 4 Weeks', 'medium_term' as 'Last 6 Months', 'long_term' as 'All Time'), and a 'Logout' button that clears `st.session_state`.
> 4. Create 3 tabs in the main view:
>    - **Tab 1 (📊 Top Stats):** Show Top 10 Tracks and Top 10 Artists side-by-side with thumbnail images and links, plus a bar chart (`st.bar_chart`) of their Top Genres using `pandas`.
>    - **Tab 2 (🔥 AI Taste Roast):** A button 'Analyze My Music Taste' that calls `get_ai_analysis_and_recs`, stores the result in `st.session_state`, and displays the `'roast_and_aura'` markdown.
>    - **Tab 3 (🎵 AI Playlist Creator):** Shows the 10 recommended songs from the AI analysis, lets the user edit the playlist title in an `st.text_input`, and provides a button 'Create Playlist on My Spotify' that calls `build_spotify_playlist` and shows a celebration (`st.balloons()`) with a clickable link to listen to their new playlist!"*

### Step 4: Run and Test Your App!
Launch your app from the terminal:
```bash
streamlit run app.py
```
1. Your browser will open `http://localhost:8501`.
2. Click **"🎧 Login with Spotify"** and approve the permissions.
3. You'll be redirected right back into your dashboard with your real listening statistics, AI roast, and playlist builder!