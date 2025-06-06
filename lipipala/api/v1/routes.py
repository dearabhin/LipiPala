from flask import Blueprint, request, jsonify
from lipipala.core.speech.service import SpeechRecognitionService
from lipipala.core.speech.exceptions import SpeechServiceError
from lipipala.config import settings

# Create a Blueprint for v1 of the API
api_v1_bp = Blueprint('api_v1', __name__, url_prefix='/api/v1')

# Initialize the service with the app's settings
speech_service = SpeechRecognitionService(settings.speech_recognition)


@api_v1_bp.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok", "version": settings.version})


@api_v1_bp.route('/speech/transcribe', methods=['POST'])
def transcribe_audio():
    if 'file' not in request.files or 'language' not in request.form:
        return jsonify({"error": "Missing 'file' or 'language' in request"}), 400

    audio_file = request.files['file']
    language = request.form['language']

    # In a real app, you would save the file temporarily
    # temp_path = f"/tmp/{audio_file.filename}"
    # audio_file.save(temp_path)

    try:
        # result = speech_service.transcribe(temp_path, language)
        # For this example, we'll fake it since we can't save files
        result = {
            'language': language,
            'text': 'Dummy transcription result.',
            'confidence': 0.9,
            'audio_duration': 5.0
        }
        return jsonify(result), 200
    except SpeechServiceError as e:
        return jsonify({"error": str(e)}), 500
    finally:
        # os.remove(temp_path) # Clean up the temp file
        pass


@api_v1_bp.route('/speech/languages', methods=['GET'])
def get_languages():
    languages = speech_service.get_supported_languages()
    return jsonify({"supported_languages": languages})
