# 🎬✨ Manimissime

**Manimissime** est un outil innovant permettant de générer automatiquement des vidéos mathématiques animées avec **Manim** à partir d'un simple prompt textuel. Ce projet exploite la puissance des LLM et une architecture multi-agents pour offrir une expérience fluide et intelligente dans la création de contenus pédagogiques.

## 🚀 Concept

Manimissime transforme vos idées en animations visuelles éducatives. Il suffit de décrire une scène mathématique ou un concept à animer, et l'outil se charge de générer le code Manim correspondant, corrige les erreurs potentielles, puis compile et produit une vidéo prête à être utilisée.

## ⚙️ Fonctionnement Technique

### Architecture Multi-agents :
1. **Agent Développeur (LangChain)** :  
   - Génère le code Manim à partir du prompt fourni.  
   - Corrige automatiquement les erreurs de syntaxe ou de logique.  
   - Relance les itérations jusqu'à obtention du code correct.

2. **Agent Analyste (LangChain)** :  
   - Évalue les résultats des animations générées.  
   - Vérifie la cohérence entre le prompt initial et la sortie.  
   - Fournit des suggestions d'améliorations ou ajuste le code en conséquence.

### Outils Utilisés :
- **Manim** : Bibliothèque d'animations mathématiques pour Python.  
- **LangChain** : Cadre de développement pour les agents conversationnels basés sur des LLMs.  
- **Python** : Langage principal de développement.

## 📽️ Exemple d'Animation

Prompt :
> Développement de Taylor d'un cosinus à l'ordre 2, 5 et 10.

![Exemple d'animation Manimissime](assets/TaylorExpansion.gif)

## 💡 Améliorations Futures

1. **Chatbot Interactif** :  
   - Intégration d'un agent conversationnel pour affiner les demandes en temps réel.  
   - Ajustement dynamique de l'animation via dialogue.

2. **Contexte Dynamique** :  
   - Réutilisation d'animations existantes pour créer des scénarios plus riches.  
   - Personnalisation des animations selon les besoins de l'utilisateur.

## 📈 Objectif

Manimissime vise à simplifier la création de vidéos éducatives, en démocratisant l'accès à des animations visuelles percutantes pour la vulgarisation scientifique et l'enseignement des mathématiques.

---

Contribuez, testez, et participez à l'amélioration de **Manimissime** !
