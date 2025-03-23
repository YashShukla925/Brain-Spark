import os
import requests
import xml.etree.ElementTree as ET
import wikipedia
import google.generativeai as genai
from fastapi import FastAPI
from dotenv import load_dotenv
from langchain.utilities import WikipediaAPIWrapper
from langchain.tools import WikipediaQueryRun
import requests

# Load API Key from .env
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Configure Google Gemini API
genai.configure(api_key=GEMINI_API_KEY)

app = FastAPI()

# Wikipedia API Wrapper
# Setup Wikipedia API Wrapper
api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=400)
wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

def query_wikipedia(query):
    try:
        result = wiki.run(query)  # This returns a string
        return {"query": query, "summary": result}  # Wrap in JSON format
    except Exception as e:
        return {"error": str(e)}

# ArXiv API Wrapper
def search_arxiv(keywords, max_results=5):
    query = keywords.replace(" ", "+")
    url = f"http://export.arxiv.org/api/query?search_query=all:{query}&start=0&max_results={max_results}"

    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch papers: {response.status_code}"}

    root = ET.fromstring(response.text)
    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title").text
        pdf_url = entry.find("{http://www.w3.org/2005/Atom}id").text.replace("abs", "pdf") + ".pdf"
        authors = [author.find("{http://www.w3.org/2005/Atom}name").text for author in entry.findall("{http://www.w3.org/2005/Atom}author")]

        papers.append({"title": title, "authors": authors, "pdf_url": pdf_url})

    return {"query": keywords, "papers": papers}

@app.get("/wikipedia/")
def wikipedia_api(query: str):
    return query_wikipedia(query)

@app.get("/arxiv/")
def arxiv_api(query: str):
    return search_arxiv(query)

@app.get("/gemini/")
def gemini_api(prompt: str):
    try:
        response = genai.chat(model="gemini-1.5-pro", messages=[{"role": "user", "content": prompt}])
        return {"query": prompt, "response": response.text}
    except Exception as e:
        return {"error": str(e)}
