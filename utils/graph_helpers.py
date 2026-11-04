import matplotlib.pyplot as plt
import networkx as nx
import streamlit as st

def verifier_coherence(graphe_poids, h, goal):
    """
    Vérifie la cohérence de l'heuristique h (h(goal) == 0 et h(a) <= g + h(c)).
    graphe_poids format: {(a, c): g}
    """
    if h.get(goal, 0) != 0:
        return False, f"h({goal}) doit être égal à 0 (valeur actuelle : {h.get(goal)})"
    
    for (a, c), g in graphe_poids.items():
        if h.get(a, 0) > g + h.get(c, 0):
            msg = f"Incohérence détectée sur l'arête ({a} -> {c}) : h({a})={h.get(a, 0)} > c({a},{c})={g} + h({c})={h.get(c, 0)}"
            return False, msg
            
    return True, "L'heuristique est cohérente !"

def convertir_en_adjacence_simple(graphe_poids):
    """
    Convertit un graphe {(u, v): coût} en liste d'adjacence simple {u: [v1, v2]}
    pour les algorithmes non-informés sans poids (BFS / DFS).
    """
    adj = {}
    for (u, v) in graphe_poids.keys():
        if u not in adj:
            adj[u] = []
        adj[u].append(v)
        if v not in adj:
            adj[v] = []
    return adj

def dessiner_graphe(graphe_poids, chemin_optimal=None, heuristiques=None):
    """
    Génère un rendu visuel du graphe avec NetworkX et Matplotlib.
    Met en évidence les nœuds et les arêtes du chemin optimal pi.
    """
    G = nx.DiGraph()
    
    for (u, v), w in graphe_poids.items():
        G.add_edge(u, v, weight=w)
        
    pos = nx.spring_layout(G, seed=42)
    
    fig, ax = plt.subplots(figsize=(8, 5))
    
    # Identifier les arêtes du chemin optimal
    edges_in_path = []
    nodes_in_path = set()
    if chemin_optimal and len(chemin_optimal) > 1:
        nodes_in_path = set(chemin_optimal)
        for i in range(len(chemin_optimal) - 1):
            edges_in_path.append((chemin_optimal[i], chemin_optimal[i+1]))
            
    # Couleurs des nœuds
    node_colors = []
    for node in G.nodes():
        if node in nodes_in_path:
            node_colors.append('#2ecc71')  # Vert pour le chemin trouvé
        else:
            node_colors.append('#3498db')  # Bleu standard
            
    # Couleurs et largeurs des arêtes
    edge_colors = []
    edge_widths = []
    for u, v in G.edges():
        if (u, v) in edges_in_path:
            edge_colors.append('#e74c3c')  # Rouge pour le chemin
            edge_widths.append(3.0)
        else:
            edge_colors.append('#bdc3c7')
            edge_widths.append(1.0)
            
    # Labels des nœuds (inclure h(n) si disponible)
    labels = {}
    for n in G.nodes():
        if heuristiques and n in heuristiques:
            labels[n] = f"{n}\n(h={heuristiques[n]})"
        else:
            labels[n] = n
            
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, node_size=1200, ax=ax)
    nx.draw_networkx_labels(G, pos, labels=labels, font_color='white', font_weight='bold', ax=ax)
    
    nx.draw_networkx_edges(G, pos, edge_color=edge_colors, width=edge_widths, arrowsize=20, ax=ax)
    
    # Affichage des poids sur les arêtes
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, ax=ax)
    
    plt.axis('off')
    return fig