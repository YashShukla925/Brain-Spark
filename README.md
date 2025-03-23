# Brain-Spark

**An AI-powered research assistant that retrieves information from Wikipedia and ArXiv based on user queries.**


## 🚀 Features
- ✅ Search Wikipedia summaries for any topic.
- ✅ Fetch academic papers from ArXiv.
- ✅ Responsive UI with a clean layout.
- ✅ Built using **Streamlit**, **FastAPI**, and **LangChain**.

## 🛠️ Tech Stack
- **Frontend:** Streamlit  
- **Backend:** FastAPI  
- **AI Tools:** LangChain (Wikipedia API Wrapper)  
- **Database:** None (fetches live data)  

## 📦 Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-username/BrainSpark.git
cd BrainSpark
```

### 2️⃣ Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Start the FastAPI Backend and streamlit app
```bash
uvicorn main:app --reload
streamlit run app.py
```

### 🖥️ Usage

- 1️⃣ Enter a topic in the search bar.
- 2️⃣ Click "Search Wikipedia" for a quick summary.
- 3️⃣ Click "Search ArXiv" to find research papers.
