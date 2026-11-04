#code Recherche Simple Profondeur

def etat(pi):
    return pi[-1]

def etats(Q):
    return {c[-1] for c in Q}

def recherche_simple_profondeur(graphe, depart, objectif):
    Q = [[depart]]
    E = set()
    it = 0

    while Q:
        pi = Q.pop()
        u = etat(pi)

        if u == objectif:
            print(f"{it}. chemin {pi} => objectif {pi[-1]} atteint")
            return pi
        
        if u != objectif:
            print(f"{it}. chemin {pi} => {pi[-1]} ≠ objectif")

        E.add(u)

        for v in graphe.get(u, []):
            pi2 = pi + [v]
            if (v not in E) : Q.append(pi2)

        it += 1

    print("Échec : aucun chemin trouvé.")
    return None