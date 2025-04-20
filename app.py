#source venv/bin/activate
import speech_recognition as sr
import pyttsx3
import requests

# Text to Speech setup
tts = pyttsx3.init()
tts.setProperty('rate', 180)

# Groq API Setup
GROQ_API_KEY = "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"
WAKE_WORD = "hey groq"  # You can change this

# Talk function
def speak(text):
    tts.say(text)
    tts.runAndWait()

# Groq API call
def chat_with_groq(prompt):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": "whisper-large-v3",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(url, headers=headers, json=data)
    return response.json()['choices'][0]['message']['content']

# Listen to microphone
def listen_to_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        audio = recognizer.listen(source, phrase_time_limit=5)
        try:
            text = recognizer.recognize_google(audio).lower()
            return text
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            print("⚠️ Speech Recognition service failed.")
            return ""

# Main loop
def main():
    print("🎧 Waiting for wake word: 'Hey Groq'")
    while True:
        # Always listen for wake word
        trigger = listen_to_audio()
        print("Heard:", trigger)

        if WAKE_WORD in trigger:
            print("🟢 Wake word detected! Listening for query...")
            speak("Yes, how can I help you?")

            user_input = listen_to_audio()
            print("🗣️ You said:", user_input)

            if user_input:
                response = chat_with_groq(user_input)
                print("🤖 Groq:", response)
                speak(response)
            else:
                speak("Sorry, I didn't catch that.")
        elif "exit" in trigger or "quit" in trigger:
            speak("Okay, exiting. Have a great day!")
            break

if __name__ == "__main__":
    main()
