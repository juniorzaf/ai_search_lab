class Node:
    def __init__(self, position, parent=None):
        self.position = position  # Tuple (ligne, colonne)
        self.parent = parent      # Nœud parent pour remonter le chemin
        self.g = 0                # Coût accumulé depuis le départ
        self.h = 0                # Estimation heuristique jusqu'à l'arrivée
        self.f = 0                # Coût total (g + h)

    def __eq__(self, other):
        return self.position == other.position

    def __lt__(self, other):
        return self.f < other.f   # Nécessaire pour les files de priorité (heapq)