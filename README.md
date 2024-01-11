# **NewsPulse**

#### [Web App Link](https://newspulse.streamlit.app/) 

## Description of the app

The connector's purpose is to connect the Streamlit web application with the News API, allowing users to retrieve and view news articles based on various parameters such as category, sort order, language, and page size.

## The connector facilitates the following functionalities:

1. **News Retrieval:** It fetches news articles from the News API based on the user's selected category, sort order, language, and page size.
2. **Streamlit Integration:** It integrates the retrieved news articles with the Streamlit web application for displaying them to the user.

## Working of the app

1. **NewsAPIConnection Class:**
The code defines a custom class called `NewsAPIConnection`, which extends the `ExperimentalBaseConnection` class from Streamlit. This class acts as a connection to the News API.
2. **Initialization:**
The `__init__` method in the `NewsAPIConnection` class sets up the connection.
3. **_connect() Method:**
The `_connect` method within the `NewsAPIConnection` class creates an HTTP session using the `requests` library, which will be used to make API requests to the News API.
4. **cursor() Method:**
The `cursor` method returns the session, allowing access to make API requests to the News API.
5. **query() Method:**
The `query` method performs the actual API call to the News API using the session and the parameters set by the user in the Streamlit web application. It sends the parameters as part of the API request, fetches the news data, and returns a list of news articles in JSON format.
