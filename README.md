# Application de Transcription et Synthèse Vocale

Cette application permet de convertir des fichiers audio (messages vocaux) en texte écrit, puis d'en générer une synthèse concise mettant en évidence les points importants.

## Fonctionnalités

- **Transcription vocale** : Conversion de fichiers audio en texte
- **Synthèse de texte** : Génération automatique d'un résumé du texte transcrit
- **Interface intuitive** : Interface web simple pour télécharger des fichiers et visualiser les résultats

## Prérequis

- Python 3.10 ou supérieur
- Flask
- SpeechRecognition
- pydub
- NLTK
- ffmpeg (pour le traitement audio)

## Installation

1. Clonez ce dépôt :
```bash
git clone <url-du-depot>
cd app_transcription_vocale
```

2. Installez les dépendances :
```bash
pip install -r requirements.txt
```

3. Installez ffmpeg (nécessaire pour le traitement audio) :
```bash
sudo apt-get update
sudo apt-get install -y ffmpeg
```

## Utilisation

1. Lancez l'application :
```bash
python app.py
```

2. Ouvrez votre navigateur et accédez à l'URL :
```
http://localhost:5000
```

3. Utilisez l'interface pour :
   - Télécharger un fichier audio (formats supportés : MP3, WAV, OGG, M4A, FLAC)
   - Lancer la transcription
   - Générer une synthèse du texte transcrit

## Structure du projet

- `app.py` : Application Flask principale
- `speech_to_text.py` : Module de transcription vocale
- `text_summarizer.py` : Module de synthèse de texte
- `templates/` : Fichiers HTML pour l'interface utilisateur
- `static/` : Fichiers statiques (JavaScript, CSS)
- `test_files/` : Fichiers de test

## Fonctionnement technique

### Transcription vocale

Le module de transcription utilise la bibliothèque SpeechRecognition avec l'API Google Speech Recognition pour convertir l'audio en texte. Le processus comprend :

1. Conversion du fichier audio en format WAV (si nécessaire)
2. Ajustement pour le bruit ambiant
3. Reconnaissance vocale
4. Retour du texte transcrit

### Synthèse de texte

Le module de synthèse utilise une approche extractive pour résumer le texte :

1. Nettoyage et prétraitement du texte
2. Division en phrases
3. Calcul de la fréquence des mots (après suppression des mots vides)
4. Attribution d'un score à chaque phrase
5. Sélection des phrases avec les scores les plus élevés
6. Réorganisation des phrases dans l'ordre original

## Déploiement

Pour déployer l'application en production :

1. Utilisez un serveur WSGI comme Gunicorn :
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. Configurez un serveur proxy comme Nginx pour servir l'application.

## Limitations

- La transcription vocale nécessite une connexion Internet (utilise l'API Google Speech Recognition)
- La qualité de la transcription dépend de la clarté de l'enregistrement audio
- La taille maximale des fichiers est limitée à 16 Mo

## Améliorations futures

- Support de langues supplémentaires
- Amélioration de l'algorithme de synthèse
- Ajout d'une option pour télécharger les résultats
- Interface utilisateur responsive pour les appareils mobiles

## Licence

Ce projet est sous licence MIT.
