# import streamlit as st
# import requests
# from langchain.utilities import WikipediaAPIWrapper
# # from langchain.chains import WikipediaQueryRun

# # FastAPI Backend URL
# FASTAPI_URL = "http://127.0.0.1:8000"

# st.title("📚 Brain Spark")

# wiki_query = st.text_input("Enter a topic for Wikipedia search:")

# col1, col2 = st.columns(2)

# # Setup Wikipedia API Wrapper
# # wiki = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
# wiki = WikipediaAPIWrapper(top_k_results=1)
# # wiki = WikipediaQueryRun(api_wrapper=api_wrapper)

# def query_wikipedia(question):
#     """Fetch Wikipedia summary for the given query."""
#     return wiki.run(question)  # Returns a string

# with col1:
#     if st.button("Search Wikipedia"):
#         if wiki_query:
#             response = query_wikipedia(wiki_query)  # Fetch Wikipedia results

#             if response:  # If response is not empty
#                 st.subheader("Wikipedia Summary")
#                 st.write(response)  # Display the summary as string
#             else:
#                 st.error("No results found on Wikipedia.")

# with col2:
#     if st.button("📄 Search ArXiv"):
#         if wiki_query:
#             response = requests.get(f"{FASTAPI_URL}/arxiv/", params={"query": wiki_query})
#             data = response.json()
#             st.write("### ArXiv Papers")
#             for paper in data.get("papers", []):
#                 st.write(f"**Title:** {paper['title']}")
#                 st.write(f"**Authors:** {', '.join(paper['authors'])}")
#                 st.write(f"📥 [Download PDF]({paper['pdf_url']})")
#         else:
#             st.warning("Enter a search query first.")

# st.write("---")



import streamlit as st
import requests
from langchain.utilities import WikipediaAPIWrapper

# FastAPI Backend URL
FASTAPI_URL = "http://127.0.0.1:8000"

st.title("📚 Brain Spark")

wiki_query = st.text_input("Enter a topic for Wikipedia search:")

# Setup Wikipedia API Wrapper
wiki = WikipediaAPIWrapper(top_k_results=1)

def query_wikipedia(question):
    """Fetch Wikipedia summary for the given query with error handling."""
    try:
        response = wiki.run(question)  # Returns a string
        if not response or response.isspace():
            return "No Wikipedia results found for this topic."
        return response
    except Exception as e:
        return f"⚠️ Error fetching Wikipedia data: {str(e)}"

# Buttons Layout with Padding
col1, col2, col3 = st.columns([2.5, 0.2, 1]) 

with col1:
    search_wiki = st.button("Search Wikipedia")

with col3:
    search_arxiv = st.button("📄 Search ArXiv")

# Full-width container for results
with st.container():
    if search_wiki and wiki_query:
        response = query_wikipedia(wiki_query)
        st.subheader("Wikipedia Summary")
        st.markdown(f"📖 **Summary:**\n\n{response}")

    if search_arxiv and wiki_query:
        try:
            response = requests.get(f"{FASTAPI_URL}/arxiv/", params={"query": wiki_query})
            data = response.json()

            st.subheader("📄 ArXiv Papers")
            if data.get("papers"):
                for paper in data["papers"]:
                    st.write(f"**📌 Title:** {paper['title']}")
                    st.write(f"👨‍🔬 **Authors:** {', '.join(paper['authors'])}")
                    st.markdown(f"📥 [Download PDF]({paper['pdf_url']})")
                    st.write("---")
            else:
                st.error("No papers found on ArXiv.")
        except Exception as e:
            st.error(f"⚠️ Error fetching ArXiv data: {str(e)}")

st.write("---")
