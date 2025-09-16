import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import playsound
import os
import sqlite3
import datetime

DB_FILE = "languages.db"
TRANSLATION_FOLDER = "translations"

# Initialize translations folder
if not os.path.exists(TRANSLATION_FOLDER):
    os.makedirs(TRANSLATION_FOLDER)

# Initialize the database with language data
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS languages (
            code TEXT PRIMARY KEY,
            name TEXT,
            speech_code TEXT
        )
    ''')
    # Insert languages if table is empty
    c.execute('SELECT COUNT(*) FROM languages')
    if c.fetchone()[0] == 0:
        languages_data = [
            ("en", "English", "en-US"),
            ("hi", "Hindi", "hi-IN"),
            ("ta", "Tamil", "ta-IN"),
            ("te", "Telugu", "te-IN"),
            ("ml", "Malayalam", "ml-IN"),
            ("kn", "Kannada", "kn-IN"),
            ("fr", "French", "fr-FR"),
            ("es", "Spanish", "es-ES"),
            ("de", "German", "de-DE"),
            ("ja", "Japanese", "ja-JP"),
            ("zh-cn", "Chinese (Simplified)", "zh-CN"),
            ("ar", "Arabic", "ar-SA"),
            ("ru", "Russian", "ru-RU")
        ]
        c.executemany('INSERT INTO languages VALUES (?, ?, ?)', languages_data)
        conn.commit()
    conn.close()

# Fetch all languages from database
def fetch_languages():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute('SELECT code, name, speech_code FROM languages')
    data = c.fetchall()
    conn.close()
    return {code: {"name": name, "speech_code": speech_code} for code, name, speech_code in data}

# Save and play audio file
def save_and_play_audio(text, lang="en"):
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{TRANSLATION_FOLDER}/translation_{timestamp}.mp3"
    tts = gTTS(text=text, lang=lang)
    tts.save(filename)
    playsound.playsound(filename)
    return filename  # return path for reference if needed

def show_languages(languages):
    print("\nAvailable Languages:")
    for code, info in languages.items():
        print(f"{code} : {info['name']}")

def main():
    init_db()
    languages = fetch_languages()
    translator = Translator()
    recognizer = sr.Recognizer()

    # Select input language
    show_languages(languages)
    src_lang = input("\nEnter INPUT language code (what you will SPEAK): ").strip()
    if src_lang not in languages:
        print("❌ Invalid input language code! Defaulting to English.")
        src_lang = "en"

    # Select output language
    show_languages(languages)
    dest_lang = input("\nEnter OUTPUT language code (what you want to HEAR): ").strip()
    if dest_lang not in languages:
        print("❌ Invalid output language code! Defaulting to English.")
        dest_lang = "en"

    print("\n🟢 Translator started! Speak 'stop' anytime to stop.\n")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        recognizer.pause_threshold = 1.5

        while True:
            try:
                print(f"🎤 Listening in {languages[src_lang]['name']}...")
                audio = recognizer.listen(source)

                # Speech to text
                text = recognizer.recognize_google(audio, language=languages[src_lang]['speech_code'])
                text_lower = text.strip().lower()
                print(f"✅ You said: {text}")

                # Stop command
                if text_lower == "stop":
                    print("\n🛑 Stop command received. Translator stopped.")
                    break

                # Translation
                translated = translator.translate(text, src=src_lang, dest=dest_lang)
                print(f"🌍 Translated ({languages[dest_lang]['name']}): {translated.text}")

                # Ask user if they want to play audio
                play_choice = input("▶️ Do you want to play the translated audio? (y/n): ").strip().lower()
                if play_choice == "y":
                    file_path = save_and_play_audio(translated.text, lang=dest_lang)
                    print(f"💾 Audio saved at: {file_path}")
                else:
                    # Save anyway if you want to keep files even without playing
                    file_path = save_and_play_audio(translated.text, lang=dest_lang)
                    print(f"💾 Audio saved at: {file_path} (not played)")

                print("\n--- Ready for next sentence ---\n")

            except sr.UnknownValueError:
                print("❌ Could not understand audio, please try again.")
                save_and_play_audio("Could not understand audio")
            except sr.RequestError as e:
                print("❌ Could not request results from Google Speech Recognition; check internet. Error:", e)
                save_and_play_audio("Network error, please check your internet")
            except Exception as e:
                print("⚠️ Unexpected error:", e)
                save_and_play_audio(f"Unexpected error: {e}")

if __name__ == "__main__":
    main()
