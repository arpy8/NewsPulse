import os
import requests
import streamlit as st
from streamlit.connections import ExperimentalBaseConnection
from streamlit.runtime.media_file_storage import MediaFileStorageError

# Constants
API_KEY = os.getenv("NEWS_API")
BASE_URL = 'https://newsapi.org/v2/everything'
DEFAULT_PAGE_SIZE = 10

# Mapping of language names to codes
LANGUAGE_DICT = {
    "English": "en",
    "Arabic": "ar",
    "German": "de",
    "Spanish": "es",
    "French": "fr",
    "Hebrew": "he",
    "Italian": "it",
    "Dutch": "nl",
    "Norwegian": "no",
    "Portuguese": "pt",
    "Russian": "ru",
    "Swedish": "sv",
    "Chinese": "zh"
}


# News API connection class
class NewsAPIConnection(ExperimentalBaseConnection):
    def __init__(self, my_connection_name):
        super().__init__(my_connection_name)

    def _connect(self):
        self.session = requests.Session()

    def cursor(self):
        return self.session

    def query(self):
        response = self.session.get(BASE_URL, params=parameters)
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
    st.write("<h1 style='text-align:center; font-size:7vh; padding-bottom:10vh'>"
             "News<span style='color:red'>Pulse</span></h1>", unsafe_allow_html=True)

    # Sidebar options
    category = st.selectbox('Category',
                            ("General", "Entertainment", "Technology", "Business", "Health", "Sports", "Science"))
    sort_by = st.selectbox('Sort by', ("Relevancy", "Popularity", "PublishedAt"))
    language = st.selectbox('Language', list(LANGUAGE_DICT.keys()))
    page_number = st.number_input('Page Size', min_value=1, max_value=50, value=DEFAULT_PAGE_SIZE,
                                  help="Changes the number of articles per page")

    # Update parameters based on selected options
    parameters = {
        'apiKey': API_KEY,
        'q': category.lower(),
        'language': LANGUAGE_DICT[language],
        'pageSize': page_number,
        'sortBy': sort_by.lower() if sort_by else None
    }

st.write(f"""
    <div style='padding:8vh 0 10vh 0'>
    <hr><hr>
    <h1 style='text-align:center; font-size:15vh; padding:2vh 0 2vh 0'>
    News<span style='color:red'>Pulse</span></h1>
    <hr><hr>
    </div>
    <h1 style='text-align:center;color:grey;'>{category} News</h1>
    <p style='text-align:center;padding:0vh 0 4vh 0;color:#262730;font-size:8vh;'>⮟</p>
    """, unsafe_allow_html=True)
# Main content layout

# News generator
connection = NewsAPIConnection("News API Connection")
try:
    for random_news in list(connection.query()):
        st.write(f"""<h2>{random_news['title']}</h2><br>""", unsafe_allow_html=True)
        try:
            if random_news["urlToImage"] is not None:
                st.image(f'{random_news["urlToImage"]}')
        except MediaFileStorageError:
            st.image(f'assets/{category}.png')
        st.write(f"""
            <h5>{random_news['description']}</h5>
            Link : <a href="{random_news['url']}">{random_news['url'][:80]}...</a><br>
            Author : {random_news['author']}, &nbsp; <i>{random_news['publishedAt'][:10]}</i>
            <hr>
            """, unsafe_allow_html=True)
except requests.exceptions.RequestException:
    st.error("Failed to fetch news data. Please check your internet connection.")
