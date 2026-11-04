import re

import streamlit as st
import ast
from utils.graph_helpers import verifier_coherence, convertir_en_adjacence_simple, dessiner_graphe

# Importatiion des algorithmes de recherche
from algorithms.depth_first_search import recherche_simple_profondeur
from algorithms.breadth_first_search import recherche_simple_largeur       
from algorithms.uniform_cost_search import recherche_cout_uniforme 
from algorithms.a_star import a_star                   

st.set_page_config(page_title="AI Search LAB", layout="wide")

st.title("AI Search LAB (Simulation des algorithmes de recherche du cours INF 5183 de l'Université du Québec en Outaouais (UQO))")
st.caption("Départ fixe : **S** | Arrivée fixe : **G** (Max 8 nœuds)")

# --- 1. SELECTION DU TYPE DE RECHERCHE ---
with st.sidebar:
    st.header("Configuration")
    
    type_recherche = st.selectbox(
        "Type de recherche",
        [
            "Recherche Simple en Largeur (BFS)",
            "Recherche Simple en Profondeur (DFS)",
            "Recherche à Coût Uniforme (UCS)",
            "Recherche A*"
        ]
    )
    
    depart = "S"
    objectif = "G"
    
    st.markdown("---")
    mode_graphe = st.radio("Source du Graphe", ["Valeurs par défaut", "Personnaliser le graphe"])

# VALEURS PAR DÉFAUT (8 NOEUDS MAX: S, A, B, C, D, E, F, G)
graphe_poids_defaut = {
    ('S', 'A'): 2,
    ('S', 'B'): 5,
    ('A', 'C'): 2,
    ('A', 'D'): 4,
    ('B', 'D'): 1,
    ('B', 'E'): 5,
    ('C', 'G'): 7,
    ('D', 'G'): 3,
    ('E', 'G'): 2
}

heuristiques_defaut = {
    'S': 6,
    'A': 5,
    'B': 3,
    'C': 6,
    'D': 2,
    'E': 2,
    'F': 4,
    'G': 0
}

# --- 3. GESTION DES ENTREES UTILISATEUR OU DEFAUT ---
col_config, col_visu = st.columns([1, 1])

with col_config:
    st.subheader("Structure des données d'entrée")
    
    # A. Gestion du Graphe (Poids ou Arêtes)
    if mode_graphe == "Valeurs par défaut":
        graphe_poids = graphe_poids_defaut
        st.info("Utilisation du graphe par défaut à 7 nœuds (S -> G).")
    else:
        st.markdown("**Définir le graphe (Max 8 nœuds : S, A, B, C, D, E, F, G)**")
        if type_recherche in ["Recherche Simple en Largeur (BFS)", "Recherche Simple en Profondeur (DFS)"]:
            prompt_txt = "Entre le dictionnaire {(u, v): 1} ou les transitions de ton graphe (8 nœuds max) :"
        else:
            prompt_txt = "Entre les arêtes et leurs poids sous le format {(u, v): poids} (8 nœuds max) :"
            
        graphe_str = st.text_area(prompt_txt, value=str(graphe_poids_defaut), height=180)
        try:
            graphe_poids = ast.literal_eval(graphe_str)
            
            # Validation de la limite de 8 nœuds max
            noeuds_detectes = set([u for u, v in graphe_poids.keys()] + [v for u, v in graphe_poids.keys()])
            if len(noeuds_detectes) > 8:
                st.error(f"Le graphe contient {len(noeuds_detectes)} nœuds. La limite est de 8 nœuds maximum !")
                st.stop()
        except Exception as e:
            st.error(f"Format de graphe invalide : {e}")
            st.stop()

    # Gestion des Heuristiques pour A*
    heuristiques = {}
    is_coherente = True
    
    if type_recherche == "Recherche A*":
        st.markdown("---")
        st.subheader("Heuristiques h(n)")
        
        mode_h = st.radio("Source des heuristiques", ["Valeurs par défaut", "Saisir mes heuristiques"])
        if mode_h == "Valeurs par défaut":
            heuristiques = heuristiques_defaut
        else:
            h_str = st.text_area("Format dictionnaire {'Noeud': valeur}", value=str(heuristiques_defaut), height=150)
            try:
                heuristiques = ast.literal_eval(h_str)
            except Exception as e:
                st.error(f"Format des heuristiques invalide : {e}")
                st.stop()
                
        # VERIFICATION DE LA COHERENCE POUR A* 
        is_coherente, msg_coherence = verifier_coherence(graphe_poids, heuristiques, objectif)
        if is_coherente:
            st.success(f"{msg_coherence}")
        else:
            st.warning(f"{msg_coherence}")

    btn_lancer = st.button("Exécuter l'algorithme", type="primary", use_container_width=True)

# EXECUTION ET AFFICHAGE
with col_visu:
    st.subheader(" Resultat et Visualisation du chemin")
    
    chemin_obtenu = None
    
    if btn_lancer:
        try:
            # la recherche simple en largeur et en profondeur : Nécessitent une liste d'adjacence simple {u: [v]}
            if type_recherche == "Recherche Simple en Largeur (BFS)":
                graphe_simple = convertir_en_adjacence_simple(graphe_poids)
                chemin_obtenu = recherche_simple_largeur(graphe_simple, depart, objectif)
                
            elif type_recherche == "Recherche Simple en Profondeur (DFS)":
                graphe_simple = convertir_en_adjacence_simple(graphe_poids)
                chemin_obtenu = recherche_simple_profondeur(graphe_simple, depart, objectif)
                
            # la recherche à coût uniforme : Nécessite le graphe avec poids {(u, v): coût}
            elif type_recherche == "Recherche à Coût Uniforme (UCS)":
                chemin_obtenu = recherche_cout_uniforme(graphe_poids, depart, objectif)
                
            # A* : Nécessite le graphe avec poids ET les heuristiques
            elif type_recherche == "Recherche A*":
                chemin_obtenu = a_star(graphe_poids, depart, objectif, heuristiques)

            # Restitution du résultat
            if chemin_obtenu:
                st.success(f"Chemin trouvé ($\pi$) : {' -> '.join(chemin_obtenu)}")
            else:
                st.error("Aucun chemin n'a été trouvé vers l'objectif G.")
                
        except Exception as e:
            st.error(f"Erreur pendant l'exécution de l'algorithme : {e}")
            
    # Affichage graphique systématique avec le chemin mis en valeur s'il existe
    fig = dessiner_graphe(graphe_poids, chemin_optimal=chemin_obtenu, heuristiques=heuristiques if type_recherche == "Recherche A*" else None)
    st.pyplot(fig)