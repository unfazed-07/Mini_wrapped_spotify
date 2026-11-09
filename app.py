"""
app.py - Streamlit UI for "My Mini Wrapped & AI DJ".

Run with:  streamlit run app.py
"""

import pandas as pd
import spotipy
import streamlit as st
from spotipy.exceptions import SpotifyException

import backend

st.set_page_config(page_title="Mini Wrapped & AI DJ", page_icon="🎧", layout="wide")


# --------------------------------------------------------------------------- #
# Helpers
# --------------------------------------------------------------------------- #
def show_spotify_error(exc: SpotifyException, action: str):
    """Turn a SpotifyException into a message a human can act on."""
    status = getattr(exc, "http_status", None)
    if status == 401:
        st.error("Your Spotify session expired. Please log out and log in again.")
    elif status == 403:
        st.error(
            f"Spotify refused to {action} (403 Forbidden). Common causes while your app is "
            "in Development Mode: the app owner needs Spotify Premium, and the account you "
            "logged in with must be added under **User Management** in the Spotify "
            "Developer Dashboard."
        )
    elif status == 429:
        st.error("Spotify is rate-limiting requests. Wait a minute and try again.")
    else:
        st.error(f"Spotify error while trying to {action}: {exc}")


def render_landing(oauth):
    """Centered login screen."""
    _, mid, _ = st.columns([1, 2, 1])
    with mid:
        st.markdown("# 🎧 My Mini Wrapped & AI DJ")
        st.markdown(
            "Don't wait for December. Log in with Spotify to see your top tracks, artists "
            "and genres, get an AI-powered **music aura check and friendly roast**, and "
            "save a fresh **AI-curated playlist** straight to your Spotify library."
        )
        st.link_button(
            "🎧 Login with Spotify",
            oauth.get_authorize_url(),
            type="primary",
            use_container_width=True,
        )
        st.caption(
            "Spotify opens in a new tab. After you approve, you'll land back here "
            "in your dashboard."
        )


def render_track_row(item: dict, index: int):
    col_img, col_txt = st.columns([1, 5])
    with col_img:
        if item.get("album_image") or item.get("image"):
            st.image(item.get("album_image") or item.get("image"), width=56)
    with col_txt:
        title = item["name"]
        if item.get("url"):
            title = f"[{title}]({item['url']})"
        subtitle = item.get("artist") or ", ".join(item.get("genres", [])[:2])
        st.markdown(f"**{index}. {title}**  \n{subtitle}")


# --------------------------------------------------------------------------- #
# Auth flow
# --------------------------------------------------------------------------- #
missing = backend.missing_config()
if missing:
    st.title("🎧 My Mini Wrapped & AI DJ")
    st.error(
        "Missing configuration in your `.env` file: **" + "**, **".join(missing) + "**.  \n"
        "Fill in your Spotify credentials, save the file, and restart the app."
    )
    st.stop()

oauth = backend.get_oauth()

# Spotify redirected back with ?code=... -> swap it for a token.
if "token_info" not in st.session_state:
    params = st.query_params
    if "code" in params:
        try:
            st.session_state["token_info"] = backend.exchange_code_for_token(
                oauth, params["code"]
            )
        except Exception as exc:  # noqa: BLE001
            st.error(f"Login failed: {exc}")
        st.query_params.clear()
    elif "error" in params:
        st.warning(f"Spotify login was cancelled or failed ({params['error']}).")
        st.query_params.clear()

if "token_info" not in st.session_state:
    render_landing(oauth)
    st.stop()

# Refresh the token if it has expired, then build the Spotify client.
try:
    st.session_state["token_info"] = backend.ensure_fresh_token(
        oauth, st.session_state["token_info"]
    )
except Exception:  # noqa: BLE001
    st.session_state.clear()
    st.warning("Your session expired. Please log in again.")
    st.rerun()

sp = spotipy.Spotify(
    auth=st.session_state["token_info"]["access_token"], requests_timeout=15, retries=2
)

# --------------------------------------------------------------------------- #
# Sidebar
# --------------------------------------------------------------------------- #
with st.sidebar:
    st.header("🎧 Mini Wrapped")
    time_range = st.selectbox(
        "Time range",
        options=list(backend.TIME_RANGES.keys()),
        format_func=lambda k: backend.TIME_RANGES[k],
        index=1,
    )

# Stats are cached per time range for this session so tab switches stay instant.
stats_cache = st.session_state.setdefault("stats", {})
if time_range not in stats_cache:
    try:
        with st.spinner("Pulling your listening history..."):
            stats_cache[time_range] = backend.get_user_stats(sp, time_range)
    except SpotifyException as exc:
        show_spotify_error(exc, "load your listening stats")
        st.stop()
stats = stats_cache[time_range]
profile = stats["profile"]
range_label = backend.TIME_RANGES[time_range]

with st.sidebar:
    if profile["image"]:
        st.image(profile["image"], width=96)
    st.subheader(profile["display_name"])
    if st.button("Logout", use_container_width=True):
        st.session_state.clear()
        st.rerun()

st.title(f"Hey {profile['display_name']} 👋")
st.caption(f"Showing: **{range_label}**")

ai_cache = st.session_state.setdefault("ai", {})
playlist_cache = st.session_state.setdefault("playlists", {})

tab_stats, tab_roast, tab_playlist = st.tabs(
    ["📊 Top Stats", "🔥 AI Taste Roast", "🎵 AI Playlist Creator"]
)

# --------------------------------------------------------------------------- #
# Tab 1: stats
# --------------------------------------------------------------------------- #
with tab_stats:
    if not stats["top_tracks"] and not stats["top_artists"]:
        st.info(
            "Spotify has no listening data for this time range yet. "
            "Listen to some music, or try a longer range."
        )
    else:
        col_tracks, col_artists = st.columns(2)
        with col_tracks:
            st.subheader("Top 10 Tracks")
            for i, track in enumerate(stats["top_tracks"], 1):
                render_track_row(track, i)
        with col_artists:
            st.subheader("Top 10 Artists")
            for i, artist in enumerate(stats["top_artists"], 1):
                render_track_row(artist, i)

        st.subheader("Most Listened Genres")
        if stats["top_genres"]:
            genre_df = pd.DataFrame(
                {"Artists": list(stats["top_genres"].values())},
                index=list(stats["top_genres"].keys()),
            )
            st.bar_chart(genre_df)
            st.caption("Number of your top artists tagged with each genre.")
        else:
            st.info("Spotify didn't return genre tags for your top artists.")

# --------------------------------------------------------------------------- #
# Tab 2: AI roast
# --------------------------------------------------------------------------- #
with tab_roast:
    st.subheader("Your Music Aura & Roast")
    if backend.ai_key_name() in backend.missing_config(include_ai=True):
        st.warning(f"Add your `{backend.ai_key_name()}` to `.env` and restart to enable AI features.")

    if st.button("Analyze My Music Taste", type="primary"):
        if not stats["top_tracks"]:
            st.info("Not enough listening data in this range to analyze.")
        else:
            try:
                with st.spinner("The AI is judging your playlists..."):
                    ai_cache[time_range] = backend.get_ai_analysis_and_recs(
                        stats["top_artists"], stats["top_tracks"]
                    )
                playlist_cache.pop(time_range, None)
            except Exception as exc:  # noqa: BLE001
                st.error(f"The AI request failed: {exc}")

    if time_range in ai_cache:
        st.markdown(ai_cache[time_range]["roast_and_aura"])
        if ai_cache[time_range].get("meta"):
            st.caption(f"Generated by {ai_cache[time_range]['meta']}")
    else:
        st.caption("Hit the button to get your aura check and roast.")

# --------------------------------------------------------------------------- #
# Tab 3: playlist maker
# --------------------------------------------------------------------------- #
with tab_playlist:
    st.subheader("1-Click AI Playlist Maker")
    if time_range not in ai_cache:
        st.info("Run **Analyze My Music Taste** in the roast tab first, then come back here.")
    else:
        recs = ai_cache[time_range]["recommendations"]
        st.markdown("**Fresh picks based on your taste:**")
        for i, song in enumerate(recs, 1):
            st.markdown(f"{i}. {song}")

        playlist_name = st.text_input(
            "Playlist title",
            value=f"Mini Wrapped Mix - {range_label}",
            key=f"playlist_name_{time_range}",
        )

        if st.button("Create Playlist on My Spotify", type="primary"):
            if not playlist_name.strip():
                st.warning("Give your playlist a title first.")
            else:
                try:
                    with st.spinner("Finding songs and building your playlist..."):
                        playlist_cache[time_range] = backend.build_spotify_playlist(
                            sp, profile["id"], playlist_name.strip(), recs
                        )
                    st.balloons()
                except SpotifyException as exc:
                    show_spotify_error(exc, "create the playlist")
                except Exception as exc:  # noqa: BLE001
                    st.error(f"Couldn't create the playlist: {exc}")

        result = playlist_cache.get(time_range)
        if result:
            st.success(f"Playlist created with {result['added']} tracks! 🎉")
            st.link_button("▶️ Open playlist in Spotify", result["url"])
            if result["missing"]:
                st.warning(
                    "Couldn't find these on Spotify, so they were skipped:\n\n"
                    + "\n".join(f"- {s}" for s in result["missing"])
                )
