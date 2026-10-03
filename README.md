<div align="center">

# ⚡ LLM-Based Autonomous Browser Agent

### An AI-powered autonomous browser agent that understands natural language and performs real browser automation using Large Language Models.

<img src="https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white"/>
<img src="https://img.shields.io/badge/Playwright-45BA4B?style=for-the-badge&logo=playwright&logoColor=white"/>
<img src="https://img.shields.io/badge/Gemini-AI-8E75B2?style=for-the-badge&logo=google&logoColor=white"/>
<img src="https://img.shields.io/badge/OpenAI-GPT--4o-412991?style=for-the-badge&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge"/>

</div>

---

# 🚀 Live Demo

> **Demo URL**

**https://llm-based-autonomous-browser-agent-ag5uffy84euk6eu5nwmeqz.streamlit.app**

> **Note:** The Streamlit deployment showcases the application's interface. Features requiring local browser control, microphone access, or system audio are designed to run in a local environment.

---

# 📖 Overview

LLM-Based Autonomous Browser Agent is an intelligent web automation system that combines **Large Language Models (LLMs)** with **Playwright browser automation** to execute real-world web tasks from simple natural language instructions.

Instead of relying on predefined automation scripts, the agent observes web pages, reasons about the current state, adapts to changes, and performs multi-step workflows autonomously.

The project demonstrates how modern LLMs can be integrated with browser automation to build next-generation AI assistants capable of interacting with real websites.

---

# ✨ Features

- 🤖 Autonomous browser automation using LLM reasoning
- 🌍 Multilingual task input with automatic translation
- 🎤 Voice command support
- 🔊 Voice response generation
- 📄 Resume parsing and profile management
- 💼 Automatic job application assistance
- 📎 Resume upload during applications
- 🔐 Secure user authentication
- 🔁 Intelligent error recovery
- ✋ Manual approval before final form submission
- 🌐 General web browsing and information retrieval
- ⚡ Modern Streamlit user interface

---

# 🎯 Supported Tasks

| Category | Example Command |
|-----------|-----------------|
| 💼 LinkedIn Jobs | Apply for this LinkedIn job |
| 🏢 Company Careers | Apply for Software Engineer at Microsoft |
| 📚 Internship Applications | Find Python internships |
| 🎓 Scholarships | Search scholarships for engineering students |
| ▶️ YouTube | Play motivational videos |
| 💬 WhatsApp | Send a message to John |
| 🌐 Web Search | Search latest AI news |
| 📊 Data Extraction | Extract information from a webpage |
| 🔍 General Tasks | Search, browse and navigate websites |

---

# 🏗️ System Architecture

```text
                         User
                           │
                           ▼
                 Streamlit Web Interface
                           │
                           ▼
                 Authentication & Profile
                           │
                           ▼
              Language Translation Layer
                           │
                           ▼
                    Task Router
        ┌──────────┬──────────┬─────────┐
        ▼          ▼          ▼         ▼
   LinkedIn     YouTube   WhatsApp  General
     Agent        Agent      Agent     Agent
        │
        ▼
 Browser Automation (browser-use + Playwright)
        │
        ▼
 OpenAI GPT-4o / Google Gemini
        │
        ▼
 Browser Actions & Responses
```

---

# 📂 Project Structure

```text
LLM-Based-Autonomous-Browser-Agent/
│
├── app.py
├── auth.py
├── llm_config.py
├── profile_builder.py
├── translator.py
├── voice_input.py
├── voice_output.py
│
├── general_agent.py
├── youtube_agent.py
├── whatsapp_agent.py
├── scholarship_agent.py
├── internship_agent.py
├── linkedin_apply_agent.py
├── company_careers_agent.py
├── data_extraction_agent.py
├── submit_agent.py
│
├── requirements.txt
├── users.json
└── README.md
```

---

# 🛠️ Technology Stack

| Layer | Technology |
|---------|------------|
| Frontend | Streamlit |
| Programming Language | Python 3.10+ |
| Browser Automation | Playwright |
| Automation Framework | browser-use |
| LLM Providers | Google Gemini, OpenAI |
| LLM Framework | LangChain |
| Translation | deep-translator |
| Voice Input | SpeechRecognition |
| Voice Output | gTTS, pyttsx3 |
| Resume Parsing | pdfplumber, pypdf |
| Authentication | SHA-256 + JSON |

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/MahalaxmiMacha/LLM-Based-Autonomous-Browser-Agent.git
cd LLM-Based-Autonomous-Browser-Agent
```

## 2. Install Dependencies

```bash
pip install -r requirements.txt
```

## 3. Install Playwright Browser

```bash
python -m playwright install chromium
```

## 4. Run Application

```bash
streamlit run app.py
```

Open your browser:

```
http://localhost:8501
```

---

# 🔑 API Key Setup

This project supports two LLM providers.

### Google Gemini

Obtain a free API key from:

https://aistudio.google.com/app/apikey

Paste the API key inside the application sidebar.

---

### OpenAI

Paste your OpenAI API key inside the sidebar.

---

# 📋 Usage

### Step 1

Create a user account.

### Step 2

Complete your personal profile.

### Step 3

Upload your resume PDF.

### Step 4

Choose an LLM provider (Gemini or OpenAI).

### Step 5

Enter your API key.

### Step 6

Describe your task in natural language.

Example:

```text
Apply for Software Engineer jobs at Google.
```

or

```text
Search engineering scholarships in India.
```

or

```text
Play Interstellar soundtrack on YouTube.
```

### Step 7

The agent launches a browser and performs the requested task.

### Step 8

Review the result and approve final submission if required.

---

# 🌟 Key Highlights

- AI-powered browser automation
- Natural language task execution
- Intelligent multi-agent routing
- Resume-aware form filling
- Voice-enabled interaction
- Secure authentication
- Human approval before submission
- Modular architecture
- Easily extensible agent framework

---

# 🚀 Future Enhancements

- Multi-agent collaboration
- Chrome Extension
- Docker Deployment
- Email Automation
- Calendar Integration
- OCR-based Form Filling
- Cloud Browser Execution
- Long-term Memory
- Agent Collaboration
- Mobile Companion Application

---

# 👩‍💻 Author

**Mahalaxmi Macha**

B.Tech Computer Science Engineering

GitHub: https://github.com/MahalaxmiMacha

---

<div align="center">

### ⭐ If you found this project useful, consider giving it a star on GitHub!

</div>
