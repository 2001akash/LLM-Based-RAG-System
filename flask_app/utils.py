import os
import requests
from bs4 import BeautifulSoup
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API keys loaded from environment variables
SERPER_API_KEY = os.getenv("SERPER_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY


def search_articles(query):
    """
    Searches for articles related to the query using Serper API.
    Returns a list of dictionaries containing article URLs, headings, and text.
    """
    articles = []
    url = f"https://serperapi.com/search?q={query}"
    
    headers = {
        "Authorization": f"Bearer {SERPER_API_KEY}",
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        
        for result in data.get('organic', []):
            article = {
                'url': result.get('link', ''),
                'heading': result.get('title', ''),
                'content': fetch_article_content(result.get('link', ''))
            }
            if article['content']:  # Only add articles with content
                articles.append(article)
    
    return articles


def fetch_article_content(url):
    """
    Fetches the article content, extracting headings and text using BeautifulSoup.
    Returns the concatenated text from headings and paragraphs.
    """
    content = ""
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Extract headings and paragraphs
            for heading in soup.find_all(['h1', 'h2', 'h3']):
                content += heading.get_text() + "\n"
            for paragraph in soup.find_all('p'):
                content += paragraph.get_text() + "\n"
    except Exception as e:
        print(f"Failed to fetch content from {url}: {e}")
    
    return content.strip()


def concatenate_content(articles):
    """
    Concatenates the content of the provided articles into a single string.
    Each article's heading and content are joined with a newline.
    """
    full_text = ""
    
    for article in articles:
        full_text += article['heading'] + "\n"
        full_text += article['content'] + "\n\n"
    
    return full_text.strip()


def generate_answer(content, query):
    """
    Generates an answer from the concatenated content using GPT-4.
    The content and the user's query are used to generate a contextual answer.
    """
    prompt = (
        f"The following is relevant information:\n{content}\n\n"
        f"Using this information, answer the following question:\n{query}"
    )
    
    try:
        response = openai.Completion.create(
            engine="gpt-4",  # You can adjust this to the model you are using
            prompt=prompt,
            max_tokens=150,
            temperature=0.7
        )
        
        answer = response.choices[0].text.strip()
        return answer
    except Exception as e:
        print(f"Failed to generate answer: {e}")
        return "Sorry, I couldn't generate an answer."
