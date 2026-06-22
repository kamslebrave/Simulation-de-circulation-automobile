# On importe la classe Simulation qui contient toute la logique du programme.
from traffic.Simulation import Simulation


# Cette condition vérifie que ce fichier est lancé directement.
# Si le fichier est importé ailleurs, le code ci-dessous ne s'exécute pas.
if __name__ == "__main__":
    # Point d'entree du programme : on crée la simulation puis on lance Tkinter.
    # On crée un objet Simulation pour préparer la fenetre, les routes, les feux et les voitures.
    simulation = Simulation()

    # On lance la boucle principale de la simulation.
    # Tkinter garde la fenetre ouverte et met l'affichage à jour.
    simulation.run()
