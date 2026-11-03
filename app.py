import streamlit as st
import numpy as np
from utils.grid import init_grid
from algorithms.a_star import a_star
from algorithms.depth_first_search import recherche_simple_profondeur_E
from algorithms.breadth_first_search import recherche_simple_largeur_E
from algorithms.uniform_cost_search import recherche_simple_uniforme_E

#configuration de la page
st.set_page_config(
    page_title="AI SEARCH LAB",
    page_icon=":robot_face:",
    layout="wide"
)
st.title("AI SEARCH LAB")
st.caption("Visualisation des algorithmes de recherche en IA sur une greille 2D.")

#initialisaiton de  l'état de la session streamlit
if "grid" not in st.session_state:
    st.session_state.grid = init_grid(12, 12)
if "start" not in st.session_state:
    st.session_state.start = (0, 0)
if "goal" not in st.session_state:
    st.session_state.goal = (11, 11)

#Barre latérale pour la configuration de la grille
with st.sidebar:
    st.hearder("Configuration de la grille")
    algo_choice = st.selectbox(
        "Choisir un algorithme de recherche", 
        ["A*", "Recherche en profondeur", "Recherche en largeur", "Recherche à coût uniforme"]
        )
    st.markdown("----")
    if st.button("Réinitialiser la grille"):
        st.session_state.grid = init_grid(12, 12)
        st.session_state.start = (0, 0)
        st.session_state.goal = (11, 11)
        st.return ()

    run_button = st.button("Lancer la recherche", type="primary")

    # Corps principal
    col1, col2 = st.columns([2,1])
    with col1:
        st.subheader("Grille de simulation")
        st.write("Légende : 🟩 Départ | 🟥 Arrivée | ⬛ Obstacle / Mur | ⬜ Chemin vide")

        # Affichage de la grille interactive via un tableau modifiable ou des métriques visuelles
        # Pour un rendu simple et fonctionnel, on affiche la matrice convertie
        grid_display = st.session_state.grid.copy()
    
        # Marquage visuel basique dans l'affichage
        st.dataframe(grid_display, use_container_width=True)

    with col2:
        st.subheader("📊 Résultats")
        metrics_placeholder = st.empty()
    
    if run_search:
        start = st.session_state.start
        goal = st.session_state.goal
        grid = st.session_state.grid
        
        path = None
        explored_count = 0
        
        # Appel de l'algorithme sélectionné
        try:
            if algo_choice == "A*":
                path, explored_count = a_star(grid, start, goal)
            elif algo_choice == "BFS (Largeur)":
                path, explored_count = breadth_first_search(grid, start, goal)
            elif algo_choice == "DFS (Profondeur)":
                path, explored_count = depth_first_search(grid, start, goal)
            elif algo_choice == "Uniform Cost Search (UCS)":
                path, explored_count = uniform_cost_search(grid, start, goal)
            
            with metrics_placeholder.container():
                st.success("Recherche terminée avec succès !")
                st.metric(label="Nœuds explorés", value=str(explored_count))
                st.metric(label="Longueur du chemin", value=str(len(path) if path else 0))
        except Exception as e:
            st.error(fErreur lors de l'exécution de l'algorithme : {e}")
    else:
        metrics_placeholder.info("Clique sur 'Lancer la recherche' pour voir les performances.")

