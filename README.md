"# PFE_TEST"
# Détection et Suivi de Visage

Ce projet implémente une application de détection et suivi de visage en temps réel à l'aide d'OpenCV. Il inclut les fonctionnalités suivantes :
- Détection de plusieurs visages.
- Zoom sur les visages détectés.
- Détection des yeux et marquage par des cercles rouges.
- Alerte sonore et visuelle si aucun visage n'est détecté pendant plus de 5 secondes.
- Sauvegarde automatique des images des visages détectés.

## Bibliothèques Utilisées
- **OpenCV** : Pour la capture vidéo, la détection de visage et d'yeux, et l'affichage des résultats.
- **Pygame** : Pour les alertes sonores.
- **OS** : Pour la gestion des fichiers et dossiers.

## Étapes pour Exécuter l'Application

1. **Installer les dépendances** :
   ```bash
   pip install opencv-python pygame

2. **Exécuter le script**
    ```bash
    python app.py
