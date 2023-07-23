import os
import requests
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.media_file_storage import MediaFileStorageError

# ✅ 1. _connect()
# ✅ 2.  query()
# ✅ 3. cursor()
# ✅ 4. @st.cache_data


# Constants
API_KEY = st.secrets["NEWS_API"]
BASE_URL = 'https://newsapi.org/v2/everything'
DEFAULT_PAGE_SIZE = 15

parameters = {
    'apiKey': API_KEY,
    'q': "everything",
    'language': "en",
    'pageSize': DEFAULT_PAGE_SIZE
}


# News API connection class
class NewsAPIConnection(ExperimentalBaseConnection):
    def __init__(self, my_connection_name):
        super().__init__(my_connection_name)

    def _connect(self):
        self.session = requests.Session()

    def cursor(self):
        return self.session

    @st.cache_data()
    def query(_self):
        response = _self.session.get(BASE_URL, params=parameters)
        if response.status_code == 200:
            return response.json()['articles']
        else:
            st.error("Failed to fetch news data.")
            return None


# Initialize Streamlit page layout
st.set_page_config(page_title="NewsPulse", page_icon=":earth_asia:", initial_sidebar_state="expanded")

# CSS style to hide Streamlit footer and menu
hide_streamlit_style = """
    <style>
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
"""
st.write(hide_streamlit_style, unsafe_allow_html=True)

# Sidebar layout
with st.sidebar:
    st.write("<h1 style='text-align:center; font-size:7vh; padding-bottom:1vh'>"
             "News<span style='color:red'>Pulse</span></h1>", unsafe_allow_html=True)
    st.write("<p style='text-align:center; color:grey;'>Made using NEWS API by <a "
             "href='https://github.com/arpy8'>arpy8</a></p>",
             unsafe_allow_html=True)

# Main content layout
st.write(f"""
    <div style='padding:8vh 0 14vh 0'>
    <hr><hr>
    <h1 style='text-align:center; font-size:15vh; padding:5vh 0 6vh 0'>
    News<span style='color:red'>Pulse</span></h1>
    <hr><hr>
    </div>
    <p style='text-align:center;padding-bottom:4vh;color:#262730;font-size:8vh;'>⮟</p>
    """, unsafe_allow_html=True)

# News generator
connection = NewsAPIConnection("News API Connection")
try:
    for random_news in list(connection.query()):
        st.write(f"""<h2>{random_news['title']}</h2><br>""", unsafe_allow_html=True)
        try:
            if random_news["urlToImage"] is not None:
                st.image(f'{random_news["urlToImage"]}')
        except MediaFileStorageError:
            st.image(f'assets/general.png')
        st.write(f"""
            <h5>{random_news['description']}</h5>
            Link : <a href="{random_news['url']}">{random_news['url'][:80]}...</a><br>
            Author : {random_news['author']}, &nbsp; <i>{random_news['publishedAt'][:10]}</i>
            <hr>
            """, unsafe_allow_html=True)
except requests.exceptions.RequestException:
    st.error("Failed to fetch news data. Please check your internet connection.")
