import numpy as np

def init_grid(rows=15, cols=15):
    """Initialise une grille vide (0: vide, 1: mur, 2: départ, 3: arrivée)."""
    grid = np.zeros((rows, cols), dtype=int)
    return grid

def get_neighbors(grid, current_pos):
    """Retourne les voisins valides (haut, bas, gauche, droite) d'une cellule."""
    rows, cols = grid.shape
    row, col = current_pos
    neighbors = []
    
    # 4 directions cardinales
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    
    for dr, dc in directions:
        r, c = row + dr, col + dc
        # Vérifie les limites de la grille et si ce n'est pas un mur (1)
        if 0 <= r < rows and 0 <= c < cols:
            if grid[r, c] != 1:
                neighbors.append((r, c))
                
    return neighbors