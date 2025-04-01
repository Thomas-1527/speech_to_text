// Mise à jour du script JavaScript pour connecter l'interface aux API backend
document.addEventListener('DOMContentLoaded', function() {
    const dropArea = document.getElementById('drop-area');
    const fileInput = document.getElementById('fileInput');
    const selectFileBtn = document.getElementById('selectFileBtn');
    const transcribeBtn = document.getElementById('transcribeBtn');
    const summarizeBtn = document.getElementById('summarizeBtn');
    const fileInfo = document.getElementById('fileInfo');
    const loader = document.getElementById('loader');
    const transcriptionBox = document.getElementById('transcriptionBox');
    const summaryBox = document.getElementById('summaryBox');
    const transcriptionResult = document.getElementById('transcriptionResult');
    const summaryResult = document.getElementById('summaryResult');
    
    let selectedFile = null;
    let transcriptionText = '';
    
    // Événements pour la sélection de fichier
    selectFileBtn.addEventListener('click', () => {
        fileInput.click();
    });
    
    fileInput.addEventListener('change', handleFileSelect);
    
    // Événements pour le drag & drop
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropArea.addEventListener(eventName, highlight, false);
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropArea.addEventListener(eventName, unhighlight, false);
    });
    
    function highlight() {
        dropArea.style.backgroundColor = '#e9f7fe';
        dropArea.style.borderColor = '#2980b9';
    }
    
    function unhighlight() {
        dropArea.style.backgroundColor = '#f8f9fa';
        dropArea.style.borderColor = '#3498db';
    }
    
    dropArea.addEventListener('drop', handleDrop, false);
    
    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length) {
            handleFiles(files);
        }
    }
    
    function handleFileSelect(e) {
        const files = e.target.files;
        handleFiles(files);
    }
    
    function handleFiles(files) {
        if (files.length > 0) {
            selectedFile = files[0];
            
            // Vérifier si c'est un fichier audio
            if (!selectedFile.type.startsWith('audio/')) {
                alert('Veuillez sélectionner un fichier audio valide.');
                resetFileSelection();
                return;
            }
            
            // Afficher les informations du fichier
            fileInfo.textContent = `Fichier sélectionné: ${selectedFile.name} (${formatFileSize(selectedFile.size)})`;
            
            // Activer le bouton de transcription
            transcribeBtn.disabled = false;
            
            // Réinitialiser les résultats précédents
            resetResults();
        }
    }
    
    function formatFileSize(bytes) {
        if (bytes < 1024) {
            return bytes + ' octets';
        } else if (bytes < 1048576) {
            return (bytes / 1024).toFixed(2) + ' Ko';
        } else {
            return (bytes / 1048576).toFixed(2) + ' Mo';
        }
    }
    
    function resetFileSelection() {
        selectedFile = null;
        fileInput.value = '';
        fileInfo.textContent = '';
        transcribeBtn.disabled = true;
        summarizeBtn.disabled = true;
    }
    
    function resetResults() {
        transcriptionBox.classList.add('hidden');
        summaryBox.classList.add('hidden');
        transcriptionResult.textContent = '';
        summaryResult.textContent = '';
        transcriptionText = '';
    }
    
    // Événement pour le bouton de transcription
    transcribeBtn.addEventListener('click', function() {
        if (!selectedFile) return;
        
        // Afficher le loader
        loader.style.display = 'block';
        
        // Créer un objet FormData pour envoyer le fichier
        const formData = new FormData();
        formData.append('file', selectedFile);
        
        // Envoyer la requête au serveur
        fetch('/transcribe', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la transcription');
            }
            return response.json();
        })
        .then(data => {
            // Cacher le loader
            loader.style.display = 'none';
            
            // Afficher la transcription
            transcriptionText = data.transcription;
            transcriptionResult.textContent = transcriptionText;
            transcriptionBox.classList.remove('hidden');
            
            // Activer le bouton de synthèse
            summarizeBtn.disabled = false;
        })
        .catch(error => {
            // Cacher le loader
            loader.style.display = 'none';
            
            // Afficher l'erreur
            alert('Erreur: ' + error.message);
        });
    });
    
    // Événement pour le bouton de synthèse
    summarizeBtn.addEventListener('click', function() {
        if (!transcriptionText) return;
        
        // Afficher le loader
        loader.style.display = 'block';
        
        // Préparer les données pour la requête
        const data = {
            text: transcriptionText,
            num_sentences: 3
        };
        
        // Envoyer la requête au serveur
        fetch('/summarize', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Erreur lors de la synthèse');
            }
            return response.json();
        })
        .then(data => {
            // Cacher le loader
            loader.style.display = 'none';
            
            // Afficher la synthèse
            summaryResult.textContent = data.summary;
            summaryBox.classList.remove('hidden');
        })
        .catch(error => {
            // Cacher le loader
            loader.style.display = 'none';
            
            // Afficher l'erreur
            alert('Erreur: ' + error.message);
        });
    });
});
