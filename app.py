import asyncio
import nest_asyncio
from tavily import AsyncTavilyClient
import pandas as pd
import re
from dateutil import parser
from datetime import datetime
from typing import List
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import plotly.express as px

# Allow nested event loops (Required for Jupyter Notebooks or IPython environments)
nest_asyncio.apply()

# Initialize the AsyncTavilyClient with your API key
tavily_client = AsyncTavilyClient(api_key="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")

def extract_date(text: str) -> str:
    if not text or text == "N/A":
        return "N/A"

    date_patterns = [
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},\s+\d{4}',
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},\s+\d{4}',
        r'\b\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}',
        r'\b\d{4}-\d{2}-\d{2}', 
        r'\b\d{1,2}/\d{1,2}/\d{2,4}', 
        r'\b\d{4}', 
        r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}', 
        r'\bQ[1-4]\s+\d{4}',  
        r'\b\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)',  
        r'\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{4}',  
        r'\b\d{1,2}-\d{1,2}\s+(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec),?\s+\d{4}',  
    ]

    current_date = datetime.now().date()
    for pattern in date_patterns:
        matches = re.findall(pattern, text)
        for match in matches:
            try:
                date = parser.parse(match, fuzzy=True).date()
                if date <= current_date:
                    return date.isoformat()
            except (ValueError, OverflowError):
                continue
    return "N/A"

def extract_publisher(content: str, blurb: str) -> str:
    publisher_patterns = [
        r'Published by ([^\n]+)',            
        r'By ([^\n]+)',                      
        r'Forbes Councils Member',           
        r'PubMed',                           
        r'World Economic Forum',             
        r'PMC',                              
        r'DynamXMedical',                    
        r'Archives',                         
        r'(?:Source|Publisher|Published by|By|From)\s*[:\-–]?\s*([^\n]+)'
    ]
    text_to_search = f"{content}\n{blurb}".lower()
    for pattern in publisher_patterns:
        match = re.search(pattern, text_to_search, re.IGNORECASE)
        if match:
            return match.group(1).strip().capitalize()
    return "N/A"

def extract_blurb(content: str, max_length: int = 250) -> str:
    if not content or content == "N/A":
        return "N/A"
    sentences = re.split(r'(?<=[.!?]) +', content.strip())
    blurb = ' '.join(sentences[:3])  
    return blurb[:max_length] + "..." if len(blurb) > max_length else blurb

async def fetch_and_extract(prompt: str) -> pd.DataFrame:
    queries = [{"query": prompt, "search_depth": "advanced", "max_results": 10, "time_range": "year"}]
    responses = await asyncio.gather(*[
        tavily_client.search(**q, include_raw_content=True, extract_depth="advanced") for q in queries
    ])
    
    results_data = []
    seen_urls = set()

    for response in responses:
        for result in response.get('results', []):
            if result.get('score', 0) > 0.5:
                url = result.get("url", "N/A")
                if url not in seen_urls and url != "N/A":
                    seen_urls.add(url)

                    raw_content = result.get("raw_content", "N/A")
                    blurb = extract_blurb(raw_content)
                    extracted_date = extract_date(raw_content)
                    publisher = extract_publisher(raw_content, blurb)

                    results_data.append({
                        "Title": result.get("title", "N/A"),
                        "URL": url,
                        "Score": result.get("score", "N/A"),
                        "Published Date": extracted_date,
                        "Publisher": publisher,
                        "Blurb": blurb
                    })

    return pd.DataFrame(results_data)

# Streamlit App
st.set_page_config(layout="wide", page_title="Literature Review Assistant for Year-to-Date Publications (Powered by Tavily API)")

st.title("Literature Review Assistant for Year-to-Date Publications (Powered by Tavily API)")

prompt = st.text_input("Enter your query:", "Advancements in AI")

if st.button("Fetch and Visualize Data"):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    df = loop.run_until_complete(fetch_and_extract(prompt))

    if not df.empty:
        st.subheader("Search Results Table")
        st.dataframe(df)

        st.subheader("Keyword Cloud")
        all_blurbs = ' '.join(df['Blurb'].dropna())
        wordcloud = WordCloud(width=400, height=200, background_color='white').generate(all_blurbs)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)