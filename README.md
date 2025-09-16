# 🎤🌍 Speech-to-Speech Real-Time Translator

A Python-based **Speech-to-Speech Real-Time Translator** that captures spoken input, translates it into the selected language, and plays the translated speech. Supports multiple languages, saves translated audio files, and allows flexible language selection from a built-in database.

---

## ✨ Features
- 🎙️ **Speech Recognition** – Recognizes spoken input in multiple languages.  
- 🌐 **Translation** – Translates speech into the desired output language.  
- 🔊 **Text-to-Speech** – Plays translated speech using Google Text-to-Speech (gTTS).  
- 💾 **Audio Saving** – Saves translated audio files with timestamps.  
- 🗃️ **SQLite Database** – Stores and manages supported language codes.  
- 🛑 **Stop Command** – Say *"stop"* to exit gracefully.  

---

## 🛠️ Tech Stack
- **Python 3**
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/)  
- [gTTS](https://pypi.org/project/gTTS/)  
- [playsound](https://pypi.org/project/playsound/)  
- [googletrans](https://pypi.org/project/googletrans/)  
- SQLite (for language database)  

---

## 🚀 Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/speech-translator.git
   cd speech-translator
