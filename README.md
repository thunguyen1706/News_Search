# Financial News Sentiment Analyzer

A tool that analyzes financial news articles and determines their sentiment impact on the market using AI sentiment analysis.

## 📑 Overview

This application fetches the latest financial news articles based on user-defined topics, analyzes their content using Google's Gemini AI, and presents sentiment analysis results in an easy-to-understand format. It helps users quickly understand market sentiment without having to read through multiple news articles.

## ✨ Features

- **Search & Retrieve**: Fetch relevant financial news articles using the Brave Search API
- **AI-Powered Analysis**: Leverage Google's Gemini AI for sophisticated sentiment analysis
- **Sentiment Classification**: Articles are classified as Very Bullish, Bullish, Neutral, Bearish, or Very Bearish
- **Confidence Scoring**: Each sentiment analysis includes a confidence score (0-10)
- **Smart Summarization**: Get concise summaries of lengthy articles
- **Key Insights Extraction**: Automatically extracts the most important points from each article
- **Interactive Visualization**: View sentiment on intuitive gauge charts
- **User-Friendly Interface**: Clean, responsive web interface built with Streamlit

## 🛠️ Technologies Used

- **Backend**: FastAPI, Python
- **Frontend**: Streamlit, Plotly
- **APIs**: 
  - Brave Search API (news retrieval)
  - Google Gemini AI (sentiment analysis)
- **Libraries**:
  - newspaper3k (article parsing)
  - plotly (data visualization)
  - python-dotenv (environment variables)

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- Brave Search API Key: [Get one here](https://brave.com/search/api/)
- Google Gemini API Key: [Get one here](https://ai.google.dev/)

### Installation

1. Clone the repository
   ```bash
   git clone https://github.com/thunguyen1706/News_Search.git
   cd News_Search
   ```

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root with your API keys
   ```
   BRAVE_API_KEY=your_brave_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   ```

### Running the Application

1. Start the backend server
   ```bash
   python sentiment-backend.py
   ```

2. In a new terminal, start the frontend application
   ```bash
   streamlit run sentiment-frontend.py
   ```

3. Open your browser and navigate to http://localhost:8501

## 📋 Usage

1. Enter a financial topic in the search box (e.g., "Bitcoin", "NYSE", "Federal Reserve")
2. Adjust the number of articles to analyze using the slider
3. Click "Analyze" to fetch and process the news articles
4. Review the sentiment analysis results, summaries, and key insights
5. Click "Read Full Article" to access the original news source if desired

## 📊 Sample Output

For each article, the application provides:
- Title and source URL
- Overall sentiment classification
- Confidence score for the sentiment analysis
- Concise summary of the main points
- 2-4 key insights explaining the sentiment choice
- Visual gauge representing the sentiment

## 🔍 Future Enhancements

- Historical sentiment tracking over time
- Export functionality for reports
- Additional visualization options
- Multi-topic comparison
- User accounts to save favorite topics and analyses
- Mobile application

## 💡 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 👥 Authors

- [Thu Nguyen](https://github.com/thunguyen1706)

## 🙏 Acknowledgements

- [Brave Search API](https://brave.com/search/api/) for providing news search capabilities
- [Google Gemini AI](https://ai.google.dev/) for powerful sentiment analysis
- [Streamlit](https://streamlit.io/) for the interactive web framework
- [FastAPI](https://fastapi.tiangolo.com/) for the efficient backend API
