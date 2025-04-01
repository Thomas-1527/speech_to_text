from flask import Flask, render_template, request, jsonify
import os
import tempfile
from werkzeug.utils import secure_filename

# Importer nos modules de transcription et de synthèse
from speech_to_text import transcribe_audio
from text_summarizer import summarize_text

app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = '/tmp/audio_uploads'
ALLOWED_EXTENSIONS = {'mp3', 'wav', 'ogg', 'm4a', 'flac'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max

# Créer le dossier d'upload s'il n'existe pas
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transcribe', methods=['POST'])
def transcribe():
    # Vérifier si un fichier a été envoyé
    if 'file' not in request.files:
        return jsonify({'error': 'Aucun fichier trouvé'}), 400
    
    file = request.files['file']
    
    # Vérifier si un fichier a été sélectionné
    if file.filename == '':
        return jsonify({'error': 'Aucun fichier sélectionné'}), 400
    
    # Vérifier si le fichier est autorisé
    if not allowed_file(file.filename):
        return jsonify({'error': 'Type de fichier non autorisé'}), 400
    
    try:
        # Sauvegarder le fichier temporairement
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        # Transcrire l'audio
        transcription = transcribe_audio(filepath)
        
        # Supprimer le fichier après traitement
        os.remove(filepath)
        
        return jsonify({'transcription': transcription})
    
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la transcription: {str(e)}'}), 500

@app.route('/summarize', methods=['POST'])
def summarize():
    # Vérifier si le texte a été envoyé
    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Aucun texte trouvé'}), 400
    
    text = request.json['text']
    
    # Vérifier si le texte est vide
    if not text or len(text.strip()) == 0:
        return jsonify({'error': 'Le texte est vide'}), 400
    
    try:
        # Nombre de phrases pour la synthèse (par défaut 3)
        num_sentences = request.json.get('num_sentences', 3)
        
        # Synthétiser le texte
        summary = summarize_text(text, num_sentences=num_sentences)
        
        return jsonify({'summary': summary})
    
    except Exception as e:
        return jsonify({'error': f'Erreur lors de la synthèse: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
