import os
import speech_recognition as sr
from pydub import AudioSegment
import tempfile

def convert_audio_to_wav(audio_file_path):
    """
    Convertit un fichier audio en format WAV pour le traitement par SpeechRecognition.
    Prend en charge différents formats d'entrée (mp3, m4a, ogg, etc.)
    """
    try:
        # Obtenir l'extension du fichier
        file_ext = os.path.splitext(audio_file_path)[1].lower()
        
        # Si c'est déjà un fichier WAV, retourner le chemin directement
        if file_ext == '.wav':
            return audio_file_path
        
        # Créer un fichier temporaire pour la sortie WAV
        temp_wav = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        temp_wav_path = temp_wav.name
        temp_wav.close()
        
        # Convertir le fichier audio en WAV
        audio = AudioSegment.from_file(audio_file_path)
        audio.export(temp_wav_path, format="wav")
        
        return temp_wav_path
    
    except Exception as e:
        print(f"Erreur lors de la conversion audio: {e}")
        return None

def transcribe_audio(audio_file_path):
    """
    Transcrit un fichier audio en texte.
    Prend en charge différents formats d'entrée grâce à la conversion préalable.
    """
    try:
        # Convertir le fichier audio en WAV si nécessaire
        wav_file_path = convert_audio_to_wav(audio_file_path)
        
        if not wav_file_path:
            return "Erreur: Impossible de convertir le fichier audio."
        
        # Initialiser le recognizer
        recognizer = sr.Recognizer()
        
        # Charger le fichier audio
        with sr.AudioFile(wav_file_path) as source:
            # Ajuster pour le bruit ambiant
            recognizer.adjust_for_ambient_noise(source)
            # Enregistrer l'audio
            audio_data = recognizer.record(source)
        
        # Supprimer le fichier temporaire si ce n'est pas le fichier original
        if wav_file_path != audio_file_path:
            os.unlink(wav_file_path)
        
        # Utiliser Google Speech Recognition pour la transcription
        text = recognizer.recognize_google(audio_data, language="fr-FR")
        return text
    
    except sr.UnknownValueError:
        return "Erreur: La parole n'a pas pu être reconnue."
    except sr.RequestError as e:
        return f"Erreur: Impossible d'accéder au service de reconnaissance vocale; {e}"
    except Exception as e:
        return f"Erreur lors de la transcription: {e}"

# Fonction pour tester la transcription
def test_transcription(audio_file_path):
    """
    Fonction de test pour vérifier la transcription d'un fichier audio.
    """
    print(f"Transcription du fichier: {audio_file_path}")
    result = transcribe_audio(audio_file_path)
    print(f"Résultat de la transcription: {result}")
    return result

if __name__ == "__main__":
    # Ce code s'exécute uniquement si le script est exécuté directement
    import sys
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        test_transcription(audio_file)
    else:
        print("Veuillez spécifier un fichier audio à transcrire.")
        print("Usage: python speech_to_text.py chemin/vers/fichier_audio")
