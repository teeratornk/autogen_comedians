# 🎭 Improv Duo: Cathy & Joe (with a Critic)

An interactive AI-powered improv comedy show featuring two comedian agents (Cathy and Joe) who perform based on audience suggestions, with real-time evaluation by a critic agent. Built with Streamlit and AutoGen (ag2).

## 📸 Screenshots

![Improv Show Interface](assets/screenshot1.png)
*Real-time improv performance with live scoring*

![Show Analysis](assets/screenshot2.png)
*Complete show analysis with scores and best lines*

## 🌟 Features

- **Interactive Improv Performance**: Two AI comedians perform improvised comedy based on user suggestions
- **Real-time Streaming**: Watch the show unfold line by line with live scoring
- **Critic Feedback System**: Each line is evaluated by an AI critic using a comedy rubric
- **Adaptive Performance**: Comedians receive and respond to critic feedback in subsequent rounds
- **Customizable Settings**: Control rounds, starting comedian, and model parameters
- **Export Functionality**: Save complete show transcripts and analytics as JSON

## 📋 Prerequisites

- Python 3.10 or higher
- Azure OpenAI API access (or OpenAI-compatible endpoint)
- API key for your chosen LLM provider

## 🚀 Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd comedians
```

2. Create a virtual environment (recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/macOS
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
   - Copy `.env.example` to `.env` (or create a new `.env` file)
   - Add your Azure OpenAI credentials:
```env
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-12-01-preview
AZURE_OPENAI_ENDPOINT=https://your-endpoint.cognitiveservices.azure.com/
AZURE_OPENAI_MODEL=your-deployment-name
```

## 🎮 Usage

1. Run the Streamlit app:
```bash
streamlit run app.py
```

2. Configure settings in the sidebar:
   - **Model Configuration**: Set API credentials and model parameters
   - **Show Settings**: Choose number of rounds and starting comedian

3. Enter an audience suggestion (e.g., "airport security", "first date", "technology")

4. Click "Run Show" to start the performance

![App Interface](assets/screenshot1.png)

5. Watch as:
   - Comedians take turns performing
   - Each line is evaluated by the critic
   - Scores and feedback appear in real-time
   - Comedians adapt based on critic feedback

![Performance Analysis](assets/screenshot2.png)

## 🏗️ Project Structure

```
comedians/
├── app.py                 # Main Streamlit application
├── models.py              # Data structures (LineEval, ShowState)
├── agents.py              # Agent creation functions
├── orchestration.py       # Show orchestration logic
├── config.py              # Configuration management
├── utils.py               # Helper functions
├── ui_components.py       # UI display components
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in repo)
└── README.md              # This file
```

## 🎯 How It Works

### Comedy Performance Flow

1. **Initialization**: Two comedian agents (Cathy and Joe) are created with improv personas
2. **Turn-based Performance**: Comedians alternate delivering lines based on:
   - The audience suggestion
   - Their partner's previous line
   - Critic feedback from their last performance
3. **Real-time Evaluation**: A critic agent evaluates each line using a rubric:
   - Relevance to suggestion (0-2 points)
   - Setup to punch coherence (0-3 points)
   - Originality (0-3 points)
   - Punch impact (0-2 points)
4. **Feedback Integration**: Comedians see their scores and adjust their performance

### Scoring System

The critic evaluates each line on a 0-10 scale:
- **8-10**: Excellent performance 🔥
- **6-7**: Good performance 👍
- **0-5**: Needs improvement 🤔

Tags are assigned to categorize the humor style (wordplay, observational, etc.)

## ⚙️ Configuration Options

### Sidebar Settings

- **Model**: LLM model/deployment name
- **API Key**: Your API credentials
- **Base URL**: API endpoint (optional)
- **Timeout**: Response timeout in seconds
- **Seed**: Random seed for reproducibility
- **Rounds**: Number of performance rounds (1-8)
- **Starter**: Which comedian goes first

### Environment Variables

- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_API_VERSION`: API version
- `AZURE_OPENAI_ENDPOINT`: Azure endpoint URL
- `AZURE_OPENAI_MODEL`: Model deployment name

## 📊 Output Format

The app provides:
- **Live Transcript**: Real-time display of comedian lines
- **Score Updates**: Immediate feedback after each line
- **Complete Analysis**: Final statistics including:
  - Detailed score table
  - Average scores per comedian
  - Best line highlight
  - JSON export with full show data

## 🐛 Troubleshooting

### Common Issues

1. **"Module not found" error**: Ensure all dependencies are installed:
   ```bash
   pip install -r requirements.txt
   ```

2. **API Key errors**: Verify your `.env` file contains valid credentials

3. **Model errors**: Ensure your model deployment name matches Azure configuration

4. **Timeout errors**: Increase the timeout value in sidebar settings

### Debug Mode

The app includes error handling with detailed traceback information. If an error occurs, check the "Detailed Error Information" expander.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/)
- Powered by [AutoGen (ag2)](https://github.com/ag2ai/ag2/tree/main)
- Uses Azure OpenAI for language generation
- Inspired by the [AI Agentic Design Patterns with AutoGen](https://www.deeplearning.ai/short-courses/ai-agentic-design-patterns-with-autogen/) course by DeepLearning.AI

## 📧 Contact

For questions or feedback, please open an issue in the repository.
