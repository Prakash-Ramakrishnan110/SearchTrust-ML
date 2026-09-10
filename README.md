# 🔍 SearchTrust ML

**An open-source verification engine powered by Google Gemini that automatically graphs and fact-checks AI hallucinations against live web search.**

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![React](https://img.shields.io/badge/react-18.x-blue.svg)

---

## 🚀 The Problem: AI Hallucinations
Modern LLMs are incredible, but they hallucinate. Even when they provide citations, a citation being present does not necessarily mean it actually supports the claim. 

**SearchTrust ML** solves this by breaking down complex AI-generated answers into atomic claims, retrieving evidence, and mapping the provenance visually.

## ✨ Features

- 🧠 **Powered by Gemini**: Uses the speed and reasoning of `gemini-1.5-flash` (or your preferred Gemini model) for claim extraction and contradiction detection.
- 🕸️ **Visual Provenance Graph**: Instantly see which claims are supported (🟩) and which are refuted (🟥) through an interactive ReactFlow node graph.
- 🔎 **Claim-Level Fact Checking**: Doesn't just look at the whole text; isolates individual claims and verifies them against source documents.
- ⚖️ **Confidence Calibration**: Automatically calculates an abstention score—alerting you when the AI simply shouldn't have answered.

## 🏗️ Architecture
1. **Query & Answer** → 2. **Claim Extraction (Gemini)** → 3. **Evidence Retrieval** → 4. **Claim-Evidence Verification** → 5. **Visual Provenance Mapping**

## ⚡ Quick Start

Get up and running locally in under 2 minutes.

### 1. Clone the repo
```bash
git clone https://github.com/Prakash-Ramakrishnan110/SearchTrust-ML.git
cd SearchTrust-ML
```

### 2. Set up your Environment
Copy the example env file and add your Google Gemini API Key.
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### 3. Run the App
SearchTrust ML comes with a convenient batch script to launch the FastAPI backend and React frontend simultaneously.

On Windows:
```bash
start.bat
```
*(On macOS/Linux, simply start the backend and frontend separately).*

- **Backend API**: `http://127.0.0.1:8000`
- **Visual Dashboard**: `http://localhost:5173`

## 💻 Usage (Visual Dashboard)
1. Navigate to **http://localhost:5173**.
2. Go to the **Evaluate** page.
3. Paste an AI-generated answer and the sources.
4. Click **Generate Trust Profile**.
5. Watch as the system extracts claims and builds the **Visual Provenance Graph**.

## 📊 Bulk Experimentation
SearchTrust ML also supports CLI-based bulk evaluations for datasets like ALCE or MS MARCO.
```bash
python scripts/experiment_runner.py --input data/your_dataset.jsonl
```

## 🤝 Contributing
This project is open-source and welcomes contributions! We are actively looking for developers passionate about AI Trust and Safety. Feel free to open an issue or submit a PR.

## 📜 License
MIT License.

---
*Built with ❤️ using Google Gemini.*
