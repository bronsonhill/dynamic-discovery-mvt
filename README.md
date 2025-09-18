# Relationship Reflection App 💕

A Streamlit application that guides users through reflective exercises about their relationship dynamics. Users select a topic, answer 5 thoughtful questions, and receive personalized insights. All responses are securely stored in Firebase Firestore.

## ✨ Features

### 🧑‍💼 User Profile Collection
- Name, age, gender, and relationship status
- Secure storage for personalized insights

### 🎯 Topic Selection
Choose from 5 carefully crafted reflection topics:
- **What really matters in conflict** - Explore underlying values in disagreements
- **How do you and your partner fight fair — or not?** - Examine conflict resolution patterns
- **What makes you feel most connected?** - Discover intimacy and bonding moments
- **What do you wish your partner knew without having to say it?** - Uncover unexpressed needs
- **How do stress and outside pressures show up in your relationship?** - Analyze external impacts

### 📝 Guided Question Flow
- 5 sequential, thoughtful questions per topic
- Progress tracking and navigation
- Previous response review for context

### 📊 Summary & Insights
- Automatic summary generation
- Pattern recognition from responses
- Complete response archive

### ⭐ Feedback System
- 1-5 star rating system
- Optional written feedback
- Topic statistics and community insights

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend/Database:** Firebase Firestore
- **AI:** OpenAI GPT-3.5-turbo for dynamic question generation
- **Language:** Python 3.8+
- **Deployment:** Streamlit Cloud ready

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Firebase project with Firestore enabled
- OpenAI API key

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd dynamic-discovery-mvt
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Firebase & OpenAI:**
   
   **Option A: Local Development**
   - Download your Firebase service account key
   - Save it as `firebase_key.json` in the project root
   - Get your OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   
   **Option B: Streamlit Cloud Deployment**
   - Copy `.streamlit/secrets.toml.example` to `.streamlit/secrets.toml`
   - Fill in your Firebase credentials
   - Add your OpenAI API key

4. **Run the application:**
   ```bash
   streamlit run app.py
   ```

## 📁 Project Structure

```
dynamic-discovery-mvt/
├── app.py                          # Main Streamlit application
├── config.py                       # Firebase configuration
├── firebase_utils.py               # Database operations
├── openai_utils.py                 # AI question generation
├── questions.py                     # Topic prompts and data
├── requirements.txt                 # Python dependencies
├── .streamlit/
│   └── secrets.toml.example        # Example secrets configuration
├── .gitignore                      # Git ignore rules
└── README.md                       # This file
```

## 🔥 Firebase Setup

### 1. Create Firebase Project
1. Go to [Firebase Console](https://console.firebase.google.com/)
2. Create a new project
3. Enable Firestore Database

### 2. Generate Service Account Key
1. Go to Project Settings > Service Accounts
2. Click "Generate new private key"
3. Save the JSON file as `firebase_key.json`

### 3. Firestore Collections

The app creates these collections automatically:

**`users`**
```json
{
  "user_id": "uuid",
  "name": "string",
  "age": "number",
  "gender": "string",
  "relationship_status": "string",
  "created_at": "timestamp"
}
```

**`responses`**
```json
{
  "response_id": "uuid",
  "user_id": "string",
  "topic": "string",
  "qa_pairs": [
    {
      "question_number": 1,
      "question": "AI-generated question text",
      "response": "User's response"
    }
  ],
  "questions": ["array of AI-generated questions"],
  "responses": ["array of user answers"],
  "summary": "AI-generated summary",
  "completed_at": "timestamp"
}
```

**`ratings`**
```json
{
  "rating_id": "uuid",
  "user_id": "string",
  "topic": "string",
  "ratings": {
    "informative": "number (1-5)",
    "engaging": "number (1-5)",
    "repeat": "number (1-5)"
  },
  "informative_rating": "number (1-5)",
  "engaging_rating": "number (1-5)",
  "repeat_rating": "number (1-5)",
  "overall_rating": "number (1-5, average)",
  "feedback": "string (optional)",
  "created_at": "timestamp"
}
```

## 🌐 Deployment

### Streamlit Cloud
1. Push your code to GitHub
2. Connect your repo to [Streamlit Cloud](https://streamlit.io/cloud)
3. Add your Firebase credentials to Streamlit secrets
4. Deploy!

### Local Development
```bash
streamlit run app.py
```

## 🎨 User Experience Flow

1. **Welcome & Profile** - Users enter basic demographic information
2. **Topic Selection** - Browse and select from 5 reflection topics
3. **Question Flow** - Answer 5 questions with navigation and progress tracking
4. **Summary** - Review insights and complete responses
5. **Feedback** - Rate the experience and provide optional feedback

## 🔮 Future Enhancements

- [ ] User authentication for session tracking
- [ ] AI-powered personalized summaries
- [ ] Visual insights and pattern analysis
- [ ] Partner sharing capabilities
- [ ] Progress tracking across sessions
- [ ] Export functionality
- [ ] Mobile-optimized interface

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

MIT License - feel free to use, modify, and distribute.


---

**Built with ❤️ for better relationships**
