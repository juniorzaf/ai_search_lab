# AI Search Lab

> Une application interactive développée avec Streamlit pour explorer, visualiser et comprendre en temps réel le comportement des algorithmes de recherche en Intelligence Artificielle.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)

---

## À propos du projet

**AI Search Lab** est un outil pédagogique et technique conçu pour démystifier la manière dont les agents intelligents parcourent des espaces d'états et résolvent des problèmes de cheminement ou d'optimisation. 

Que tu sois étudiant en IA, développeur ou simplement curieux, cette application permet de comparer visuellement l'efficacité, la vitesse et la pertinence de différents algorithmes classiques.

---

## Fonctionnalités principales

* **Génération interactive de grilles / labyrinthes** : Place des obstacles, définis un point de départ et une arrivée.
* **Algorithmes non-informés (Aveugles)** :
  * Recherche en Largeur (*BFS - Breadth-First Search*)
  * Recherche en Profondeur (*DFS - Depth-First Search*)
  * Algorithme de Dijkstra
* **Algorithmes informés (Heuristiques)** :
  * Recherche Gloutonne (*Greedy Best-First Search*)
  * Algorithme $A^*$ (A-Star)
* **Tableau de bord comparatif en temps réel** : Suivi du nombre de nœuds explorés, de la longueur du chemin trouvé et du temps d'exécution.
* **Contrôles de lecture** : Animation pas à pas ou en continu pour observer l'évolution de la frontière de recherche.

---

## Structure du projet

```text
ai-search-visualizer/
│
├── algorithms/                  # Implémentation pure des algorithmes de recherche
│   ├── __init__.py
│   ├── unguided.py              # BFS, DFS, Dijkstra
│   └── heuristic.py             # A*, Greedy Best-First
│
├── utils/                       # Fonctions utilitaires, grilles et rendu
│   ├── __init__.py
│   └── grid_generator.py
│
├── tests/                       # Tests unitaires
│   └── test_algorithms.py
│
├── app.py                       # Point d'entrée de l'application Streamlit
├── requirements.txt             # Dépendances du projet
└── README.md                    # Documentation