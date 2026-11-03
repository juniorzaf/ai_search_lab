# recherche coût uniforme

def pop_min(Q):
    i_min = 0
    c_min = Q[i_min][0]
    for i, (c, _) in enumerate(Q):
        if c < c_min:                  # égalité -> on garde le plus ancien
            i_min, c_min = i, c
    return Q.pop(i_min)

def recherche_cout_uniforme(graphe, depart, objectif):
    voisins = {} # Prépare la liste des voisins sortants à partir de 'graphe'
    for (u, v), w in graphe.items():
        voisins.setdefault(u, []).append(v)

    Q = [(0, [depart])]            # frontière: (coût cumulé, chemin)
    best = {depart: 0}             # meilleur coût connu pour chaque état

    while Q:
        c, pi = pop_min(Q)
        u = pi[-1]

        if c > best.get(u, float("inf")):# entrée obsolète ?
            continue

        if u == objectif:
            print("objectif {pi[-1]} atteint")
            return pi, c

        for v in sorted(voisins.get(u, [])):
            nv = c + graphe[(u, v)]
            if ((v not in pi) and nv < best.get(v, float("inf"))):
                best[v] = nv
                Q.append((nv, pi + [v]))

    return None, float("inf")