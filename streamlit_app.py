import streamlit as st
import os
import tempfile
from speech_to_text import transcribe_audio
from text_summarizer import summarize_text

# Configuration de la page Streamlit
st.set_page_config(
    page_title="Application de Transcription et Synthèse Vocale",
    page_icon="🎤",
    layout="centered"
)

# Titre et description de l'application
st.title("Transcription et Synthèse Vocale")
st.markdown("""
Cette application vous permet de convertir un fichier audio (message vocal) en texte, 
puis d'en générer une synthèse concise mettant en évidence les points importants.
""")

# Fonction pour traiter le fichier audio
def process_audio_file(uploaded_file):
    # Créer un fichier temporaire pour stocker l'audio
    with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{uploaded_file.name.split(".")[-1]}') as tmp_file:
        # Écrire le contenu du fichier téléchargé dans le fichier temporaire
        tmp_file.write(uploaded_file.getvalue())
        tmp_file_path = tmp_file.name
    
    try:
        # Transcrire l'audio
        with st.spinner('Transcription en cours...'):
            transcription = transcribe_audio(tmp_file_path)
        
        # Afficher la transcription
        st.subheader("Transcription")
        st.write(transcription)
        
        # Ajouter un bouton pour générer la synthèse
        if st.button("Générer une synthèse"):
            with st.spinner('Génération de la synthèse en cours...'):
                # Nombre de phrases pour la synthèse
                num_sentences = st.slider("Nombre de phrases dans la synthèse", 1, 10, 3)
                
                # Synthétiser le texte
                summary = summarize_text(transcription, num_sentences=num_sentences)
                
                # Afficher la synthèse
                st.subheader("Synthèse")
                st.write(summary)
    
    except Exception as e:
        st.error(f"Erreur lors du traitement du fichier audio: {str(e)}")
    
    finally:
        # Supprimer le fichier temporaire
        if os.path.exists(tmp_file_path):
            os.unlink(tmp_file_path)

# Interface principale
st.subheader("Téléchargez votre fichier audio")
uploaded_file = st.file_uploader("Choisissez un fichier audio", type=["mp3", "wav", "ogg", "m4a", "flac"])

# Traiter le fichier s'il est téléchargé
if uploaded_file is not None:
    st.audio(uploaded_file, format=f"audio/{uploaded_file.name.split('.')[-1]}")
    
    # Afficher les informations du fichier
    file_details = {
        "Nom du fichier": uploaded_file.name,
        "Type de fichier": uploaded_file.type,
        "Taille": f"{uploaded_file.size / 1024:.2f} KB"
    }
    st.write("Détails du fichier:")
    for key, value in file_details.items():
        st.write(f"- {key}: {value}")
    
    # Bouton pour lancer le traitement
    if st.button("Transcrire"):
        process_audio_file(uploaded_file)

# Informations supplémentaires
with st.expander("À propos de cette application"):
    st.markdown("""
    ### Fonctionnement
    
    Cette application utilise deux technologies principales :
    
    1. **Reconnaissance vocale** : Conversion de l'audio en texte à l'aide de la bibliothèque SpeechRecognition
    2. **Synthèse de texte** : Extraction des phrases les plus importantes du texte transcrit
    
    ### Formats supportés
    
    L'application prend en charge les formats audio suivants :
    - MP3
    - WAV
    - OGG
    - M4A
    - FLAC
    
    ### Limitations
    
    - La qualité de la transcription dépend de la clarté de l'enregistrement audio
    - La taille maximale des fichiers est limitée
    """)

# Pied de page
st.markdown("---")
st.markdown("Développé avec Streamlit • 2025")
