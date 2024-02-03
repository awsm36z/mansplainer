from flask import Flask, request, jsonify
import speech_recognition as sr
from pydub import AudioSegment
import io

app = Flask(__name__)

@app.route('/recognize', methods=['POST'])
def recognize_speech():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    # Convert the audio file to WAV
    audio = AudioSegment.from_file(file)
    audio = audio.set_frame_rate(16000).set_channels(1)  # Convert to mono and 16000 Hz frame rate for better compatibility
    buffer = io.BytesIO()
    audio.export(buffer, format="wav")
    buffer.seek(0)

    recognizer = sr.Recognizer()
    with sr.AudioFile(buffer) as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data)
            return jsonify({"recognized_text": text}), 200
        except sr.UnknownValueError:
            return jsonify({"error": "Could not understand the audio"}), 400
        except sr.RequestError as e:
            return jsonify({"error": f"Could not request results from Google Web Speech API; {e}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
