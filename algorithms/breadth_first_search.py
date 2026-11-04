# code largeur avec E 

def etats(Q):
    return {c[-1] for c in Q}

def recherche_simple_largeur(graphe, depart, objectif):
    Q = [[depart]]
    E = set()

    while Q:
        pi = Q.pop(0)
        u = pi[-1]

        if u == objectif:
            print(f"chemin {pi} => objectif {pi[-1]} atteint")
            return pi
        
        if u != objectif:
            print(f"chemin {pi} => {pi[-1]} ≠ objectif")
            print(f"Q={Q} et E={E}")

        E.add(u)

        for v in graphe.get(u, []):
            pi2 = pi + [v]
            if v not in E : Q.append(pi2) 

    print("Échec : aucun chemin trouvé.")
    return None