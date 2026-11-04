# Etape 1: Définition de pop_min
def pop_min(Q):
    """
    Retire et retourne l'élément avec le coût minimal de la file de priorité Q.
    
    Args:
        Q (list): une liste de triplets [(f,g, chemin),(...), ...] où f=g+h est le coût estimé total, g est le coût réel, et le chemin est une liste de caractères.
        Exemple: supposons que Q=[2As, 5Bs] avec heuristiques h(A)=3, h(B)=1.
        En python : Q=[(5,2,['S','A']),(6,5,['S','B'])] donc
          Q[0][0]=5, est le coût estimé.
            Q[0][1]=2,est le coût réel.
             Q[0][2]=['S','A'] est le chemin.
        
    Returns:
        tuple: L'élément avec le coût minimal.
        
    Raises:
        ValueError: Si la file de coût est vide.
    """
    if not Q:
        raise ValueError("La frontière est vide.")
    
    # Trouver l'index de l'élément avec le coût minimal
    i_min= 0
    c_min=Q[i_min][0]
    for i, (c, *_) in enumerate(Q):
        if c < c_min:
            i_min,c_min = i, c
            
    # Retirer et retourner l'élément avec le coût minimal
    return Q.pop(i_min)

# Etape 2: Définition est_coherente
def est_coherente(graphe, h,goal):
    """
    Vérifie si l'heuristique h est cohérente pour le graphe donné.
    
    Args:
        graphe (dict): un dictionnaire représentant le graphe sous forme de liste d'adjacence.
        h (dict): un dictionnaire représentant l'heuristique pour chaque nœud.
        goal (str): le nœud objectif.
        
    Returns:
        bool: True si l'heuristique est cohérente, False sinon.
    """
    if h.get(goal, 0) != 0:
        return False
    for (a,c), g in graphe.items():
        if h.get(a, 0) > g + h.get(c,0):
            return False
    return True

# Etape 3: Définition de a_star
def a_star(graphe:dict, h:dict, goal:str, start:str):
    """
    Implémente l'algorithme A* pour trouver le chemin le plus court dans un graphe.
    
    Args:
        graphe (dict): un dictionnaire représentant le graphe sous forme de liste d'adjacence.
        h (dict): un dictionnaire représentant l'heuristique pour chaque nœud.
        start (str): le nœud de départ.
        goal (str): le nœud objectif.
    """
    voisins={}

    for(u,v),w in graphe.items():
        voisins.setdefault(u,[]).append(v)
        if not est_coherente(graphe,h,goal):
            raise ValueError("Non cohérente: h[goal]=0 et h(u)<=w(u->v)+h(v)")
        Q=[(h[start],0,[start])]
        best_g={start:0}
        E=set()
        while Q:
            f,g,chemin=pop_min(Q)
            u=chemin[-1]
            if g>best_g.get(u,float('inf')):
                continue
            if u==goal:
                return chemin
            E.add(u)
            for v in voisins.get(u,[]):
                if v in E:
                    continue
                ng=g+graphe[(u,v)]
                if v not in chemin and (ng<best_g.get(v,float('inf'))):
                    best_g[v]=ng
                    nf=ng+h[v]
                    Q.append((nf,ng,chemin+[v]))
    return None, float
