import os
import wave
import numpy as np
from pydub import AudioSegment
from pydub.generators import Sine

def generate_test_audio(output_path, text="Ceci est un message test pour vérifier la transcription vocale", duration_ms=3000, sample_rate=44100):
    """
    Génère un fichier audio de test avec un bip sonore.
    Comme nous ne pouvons pas générer de la parole directement, nous créons un fichier audio
    qui servira de placeholder pour tester le pipeline de traitement.
    
    Note: Ce fichier ne contiendra pas de parole réelle, mais permettra de tester
    le flux de traitement des fichiers audio.
    """
    # Créer un son de test (bip)
    sine_wave = Sine(440)  # 440 Hz = La
    audio = sine_wave.to_audio_segment(duration=duration_ms)
    
    # Ajouter un silence au début et à la fin
    silence = AudioSegment.silent(duration=500)
    audio = silence + audio + silence
    
    # Exporter en format wav
    audio.export(output_path, format="wav")
    
    # Ajouter des métadonnées pour indiquer le texte attendu
    with open(f"{output_path}.txt", "w") as f:
        f.write(f"Texte attendu pour ce test: {text}\n")
        f.write("Note: Ce fichier audio ne contient pas de parole réelle, mais sert à tester le pipeline de traitement.")
    
    return output_path

if __name__ == "__main__":
    output_dir = "/home/ubuntu/app_transcription_vocale/test_files"
    os.makedirs(output_dir, exist_ok=True)
    
    # Générer quelques fichiers de test
    test_file1 = os.path.join(output_dir, "test_audio_court.wav")
    test_file2 = os.path.join(output_dir, "test_audio_long.wav")
    
    generate_test_audio(test_file1, "Ceci est un message test court", 2000)
    generate_test_audio(test_file2, "Ceci est un message test plus long qui devrait contenir plusieurs phrases pour tester la capacité de transcription sur un contenu plus élaboré", 5000)
    
    print(f"Fichiers de test générés dans {output_dir}")
