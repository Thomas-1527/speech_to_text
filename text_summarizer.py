import re
import heapq

class TextSummarizer:
    def __init__(self):
        """
        Initialise le résumeur de texte avec une approche simplifiée
        qui ne dépend pas des ressources linguistiques spécifiques de NLTK.
        """
        # Liste des mots vides en français (stop words)
        self.stop_words = set([
            'le', 'la', 'les', 'un', 'une', 'des', 'et', 'est', 'sont', 'de', 'du', 'en',
            'à', 'au', 'aux', 'ce', 'ces', 'cette', 'pour', 'par', 'sur', 'dans', 'avec',
            'qui', 'que', 'quoi', 'dont', 'où', 'comment', 'pourquoi', 'quand', 'quel',
            'quelle', 'quels', 'quelles', 'mais', 'ou', 'et', 'donc', 'or', 'ni', 'car',
            'si', 'alors', 'ainsi', 'cependant', 'néanmoins', 'toutefois', 'pourtant'
        ])
    
    def _clean_text(self, text):
        """
        Nettoie le texte en supprimant les caractères spéciaux et les espaces supplémentaires.
        
        Args:
            text (str): Texte à nettoyer
            
        Returns:
            str: Texte nettoyé
        """
        # Remplacer les retours à la ligne par des espaces
        text = re.sub(r'\n+', ' ', text)
        # Supprimer les caractères spéciaux et les chiffres
        text = re.sub(r'[^\w\s\.]', ' ', text)
        # Supprimer les espaces multiples
        text = re.sub(r'\s+', ' ', text)
        return text.strip()
    
    def _split_into_sentences(self, text):
        """
        Divise le texte en phrases en utilisant des règles simples.
        
        Args:
            text (str): Texte à diviser
            
        Returns:
            list: Liste des phrases
        """
        # Diviser le texte en phrases en utilisant des points comme séparateurs
        # Mais en évitant de diviser sur les abréviations courantes
        text = text.replace('M.', 'M_DOT_')
        text = text.replace('Mme.', 'Mme_DOT_')
        text = text.replace('Dr.', 'Dr_DOT_')
        text = text.replace('etc.', 'etc_DOT_')
        
        # Diviser sur les points suivis d'un espace et d'une majuscule
        sentences = re.split(r'\.(?=\s+[A-Z])', text)
        
        # Restaurer les abréviations
        sentences = [s.replace('M_DOT_', 'M.').replace('Mme_DOT_', 'Mme.').replace('Dr_DOT_', 'Dr.').replace('etc_DOT_', 'etc.') for s in sentences]
        
        # Nettoyer les phrases
        sentences = [s.strip() + '.' if not s.strip().endswith('.') else s.strip() for s in sentences]
        
        return sentences
    
    def _split_into_words(self, sentence):
        """
        Divise une phrase en mots.
        
        Args:
            sentence (str): Phrase à diviser
            
        Returns:
            list: Liste des mots
        """
        # Convertir en minuscules et diviser sur les espaces
        words = sentence.lower().split()
        
        # Nettoyer les mots (supprimer la ponctuation)
        words = [re.sub(r'[^\w]', '', word) for word in words]
        
        # Filtrer les mots vides
        words = [word for word in words if word and word not in self.stop_words]
        
        return words
    
    def _calculate_sentence_scores(self, sentences, word_frequencies):
        """
        Calcule un score pour chaque phrase basé sur la fréquence des mots.
        
        Args:
            sentences (list): Liste des phrases du texte
            word_frequencies (dict): Dictionnaire des fréquences de mots
            
        Returns:
            dict: Dictionnaire des scores de phrases
        """
        sentence_scores = {}
        
        for sentence in sentences:
            # Ignorer les phrases trop courtes
            words = self._split_into_words(sentence)
            if len(words) <= 3:
                continue
                
            # Calculer le score de la phrase
            for word in words:
                if word in word_frequencies:
                    if sentence not in sentence_scores:
                        sentence_scores[sentence] = word_frequencies[word]
                    else:
                        sentence_scores[sentence] += word_frequencies[word]
        
        return sentence_scores
    
    def summarize(self, text, num_sentences=3):
        """
        Génère un résumé extractif du texte fourni.
        
        Args:
            text (str): Texte à résumer
            num_sentences (int): Nombre de phrases à inclure dans le résumé
            
        Returns:
            str: Texte résumé
        """
        if not text or len(text.strip()) < 100:
            return "Le texte est trop court pour être résumé."
        
        try:
            # Nettoyer le texte
            cleaned_text = self._clean_text(text)
            
            # Diviser le texte en phrases
            sentences = self._split_into_sentences(cleaned_text)
            
            # Si le nombre de phrases est inférieur ou égal au nombre demandé, retourner le texte original
            if len(sentences) <= num_sentences:
                return text
            
            # Calculer la fréquence des mots
            word_frequencies = {}
            for sentence in sentences:
                for word in self._split_into_words(sentence):
                    if word not in word_frequencies:
                        word_frequencies[word] = 1
                    else:
                        word_frequencies[word] += 1
            
            # Normaliser les fréquences
            max_frequency = max(word_frequencies.values()) if word_frequencies else 1
            for word in word_frequencies:
                word_frequencies[word] = word_frequencies[word] / max_frequency
            
            # Calculer les scores des phrases
            sentence_scores = self._calculate_sentence_scores(sentences, word_frequencies)
            
            # Obtenir les phrases avec les scores les plus élevés
            summary_sentences = heapq.nlargest(num_sentences, sentence_scores, key=sentence_scores.get)
            
            # Réorganiser les phrases dans l'ordre original
            ordered_summary = [sentence for sentence in sentences if sentence in summary_sentences]
            
            # Joindre les phrases pour former le résumé
            summary = ' '.join(ordered_summary)
            
            return summary
        
        except Exception as e:
            return f"Erreur lors de la synthèse: {e}"

def summarize_text(text, num_sentences=3):
    """
    Fonction utilitaire pour résumer un texte.
    
    Args:
        text (str): Texte à résumer
        num_sentences (int): Nombre de phrases à inclure dans le résumé
        
    Returns:
        str: Texte résumé
    """
    summarizer = TextSummarizer()
    return summarizer.summarize(text, num_sentences)

# Fonction pour tester la synthèse
def test_summarization():
    """
    Fonction de test pour vérifier la synthèse de texte.
    """
    # Texte de test (un article fictif)
    test_text = """
    La transition énergétique est devenue un enjeu majeur pour les pays du monde entier face au changement climatique. 
    Les gouvernements multiplient les initiatives pour réduire leur dépendance aux énergies fossiles et développer les énergies renouvelables.
    L'énergie solaire connaît une croissance exponentielle, avec des coûts de production qui ont chuté de plus de 80% en dix ans.
    Les éoliennes se déploient sur terre et en mer, offrant une alternative de plus en plus compétitive aux centrales à charbon ou à gaz.
    La mobilité électrique progresse également, avec des ventes de véhicules électriques qui augmentent chaque année.
    Cependant, ces transitions posent de nombreux défis, notamment en termes d'infrastructures, de stockage d'énergie et d'acceptabilité sociale.
    Les réseaux électriques doivent être modernisés pour intégrer ces nouvelles sources d'énergie intermittentes.
    Des technologies de stockage, comme les batteries ou l'hydrogène, sont en développement pour pallier cette intermittence.
    Par ailleurs, certaines populations s'inquiètent de l'impact visuel des éoliennes ou du coût de ces transitions.
    Malgré ces défis, la nécessité de réduire les émissions de gaz à effet de serre pour limiter le réchauffement climatique rend ces transformations incontournables.
    Les experts s'accordent à dire que les prochaines années seront décisives pour réussir cette transition énergétique mondiale.
    """
    
    print("Texte original:")
    print(test_text)
    print("\nRésumé:")
    summary = summarize_text(test_text, num_sentences=3)
    print(summary)
    
    return summary

if __name__ == "__main__":
    test_summarization()
