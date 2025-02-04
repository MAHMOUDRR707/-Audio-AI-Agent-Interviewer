# Audio AI Interviewer - Automated Technical Assessment System

🚀 **Automate the technical interview process using AI-powered speech-to-text, text-to-speech, and evaluation models!**  

---

## 📌 Overview  
The **Audio AI Interviewer** is an AI-driven system that conducts and evaluates technical interviews **automatically**. The system takes **predefined interview questions**, converts them into **speech**, records **candidate responses**, transcribes them into **text**, and evaluates the answers based on **AI-driven scoring metrics**. The final results are stored in **structured reports**, and candidates are **ranked based on performance**.  

### 🔹 Key Features  
✅ Converts **text questions** to **audio** (TTS)  
✅ Records **candidate responses** (45-second limit)  
✅ Converts **speech to text** (STT)  
✅ Uses **AI-based evaluation** to score responses  
✅ Generates **reports** and **ranks candidates**  

---

## 🛠️ System Workflow  

1️⃣ **Load Questions**: Reads predefined questions from a JSON file.  
2️⃣ **Text-to-Speech (TTS)**: Converts text into an audio file for candidate playback.  
3️⃣ **Play Audio & Record Response**: Plays the question audio and records the candidate's response.  
4️⃣ **Speech-to-Text (STT)**: Converts the recorded response into text.  
5️⃣ **Evaluation & Scoring**: AI model scores the response based on predefined competencies.  
6️⃣ **Report Generation**: Saves evaluation results in structured reports (CSV format).  
7️⃣ **Ranking Candidates**: Ranks candidates based on final scores.  

---

## 📂 Project Structure  

📦 Audio-AI-Interviewer │── 📂 Dataset │ ├── questions.json # Predefined interview questions │ │── 📂 Modules │ ├── text_to_speech.py # Converts text to speech │ ├── speech_to_text.py # Converts audio response to text │ ├── evaluation.py # AI-based scoring and ranking │ ├── record_audio.py # Records candidate answers │ ├── report_generator.py # Generates reports │ │── 📂 Reports │ ├── report.csv # Final evaluation report │ │── main.py # Main script to run the system │── requirements.txt # Dependencies │── README.md # Documentation │── config.py # Configuration settings



---

## 🔧 Installation & Setup  

### 1️⃣ Prerequisites  
Make sure you have the following installed:  
✅ Python **3.8+**  
✅ `pip` package manager  

### 2️⃣ Clone the Repository  
```bash
git clone https://github.com/your-username/Audio-AI-Interviewer.git
cd Audio-AI-Interviewer

```
3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 🚀 Usage
1️⃣ Run the Interview Process
```bash
python main.py
```