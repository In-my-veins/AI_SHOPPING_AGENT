# AI Shopping Agent

A Streamlit shopping assistant that searches a local product catalog, compares customer ratings, accepts product images, and places orders in a SQLite database.

## Requirements

- Python 3.10 or newer
- A Groq API key

## Setup

1. Create and activate a virtual environment.
2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in this directory:

   ```env
   GROQ_API_KEY=your_groq_api_key
   ```

4. Start the app:

   ```bash
   streamlit run app.py
   ```

The included `store.db` is the sample SQLite catalog and order store. The app reads and writes this database at runtime.
