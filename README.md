
# Tavily API Project

A Literature Review Assistant for Year-to-Date Publications powered by the Tavily API. Built using Streamlit for easy visualization of data.

## Features
- Fetches publication data using Tavily API.
- Visualizes results with a keyword cloud.
- Displays a data table with relevant results.

## Installation
Clone the repository and install dependencies:
```bash
git clone https://github.com/YourUsername/Tavily_API_Project.git
cd Tavily_API_Project
pip install -r requirements.txt
```

## Summary of Code: Literature Review Assistant for Year-to-Date Publications (Powered by Tavily API)

### Overview
This Streamlit application allows you to quickly search and visualize recent academic or online publications from the Tavily API. It provides visualizations including a keyword cloud and search results table.

### Features
1. Search Results Table: Displays search results with columns: Title, URL, Score, Published Date, Publisher, and Blurb.
2. Keyword Cloud: Generates a keyword cloud based on all collected blurbs from the search results.
3. Automated Data Extraction: Extracts publication dates, publishers, and summaries (blurbs) from the raw content using regex and text processing.
4. Visual Dashboard Interface: Built with Streamlit for easy and interactive visualization.

### Dependencies
Make sure you have all the necessary packages installed:
```
streamlit tavily pandas matplotlib seaborn plotly wordcloud nest_asyncio
```

### File Structure
```
Project_Folder/
│
├── app.py               # Your Streamlit application script (code above)
├── requirements.txt     # For deployment (optional)
├── README.md            # Project documentation (optional)
```

### How the Code Works
1. **Initialization**:
   - Imports required libraries: pandas, streamlit, plotly, seaborn, matplotlib, and wordcloud.
   - Initializes the TavilyClient with your API key for data fetching.
2. **Functions**:
   - `extract_date()`: Extracts dates from raw text.
   - `extract_publisher()`: Extracts publisher names from raw text.
   - `extract_blurb()`: Extracts short blurbs from raw text.
   - `fetch_and_extract()`: Asynchronously fetches data from the Tavily API and processes the results.
3. **Visualization (via Streamlit)**:
   - Displays a DataFrame with search results.
   - Generates a keyword cloud from the blurbs of collected search results.

### How to Run the Application
1. Navigate to Your Project Directory (e.g., `C:\Users\Cedric Attias\Tavily`)
2. Run Your Streamlit App on Anaconda Prompt
```bash
streamlit run app.py
```
3. View the App
   - The app will run on `localhost:8501` by default.
   - Open your browser and visit: [http://localhost:8501/](http://localhost:8501/)

### Usage
- Enter a query in the text input box (e.g., "Advancements in AI").
- Click the button "Fetch and Visualize Data".
- The app will display a table of results and generate a keyword cloud.
