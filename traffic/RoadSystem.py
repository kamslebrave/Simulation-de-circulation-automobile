# La classe RoadSystem sert a dessiner les routes du carrefour.
class RoadSystem:
    def __init__(self, canvas=None):
        # On garde une reference vers le canvas Tkinter.
        self.canvas = canvas

        # Si un canvas est donne, on dessine directement les routes.
        if self.canvas is not None:
            self.drawRoads()

    def drawRoads(self, canvas=None):
        # Si un nouveau canvas est donne, on l'utilise.
        if canvas is not None:
            self.canvas = canvas

        # Si aucun canvas n'existe, on affiche seulement un message console.
        if self.canvas is None:
            print("Affichage des routes")
            return

        # Dessin de la route verticale.
        self.canvas.create_rectangle(350, 0, 450, 600, fill="#4b4b4b", outline="")

        # Dessin de la route horizontale.
        self.canvas.create_rectangle(0, 250, 800, 350, fill="#4b4b4b", outline="")

        # Ligne discontinue sur la partie haute de la route verticale.
        self.canvas.create_line(400, 0, 400, 250, fill="white", dash=(16, 12), width=2)

        # Ligne discontinue sur la partie basse de la route verticale.
        self.canvas.create_line(400, 350, 400, 600, fill="white", dash=(16, 12), width=2)

        # Ligne discontinue sur la partie gauche de la route horizontale.
        self.canvas.create_line(0, 300, 350, 300, fill="white", dash=(16, 12), width=2)

        # Ligne discontinue sur la partie droite de la route horizontale.
        self.canvas.create_line(450, 300, 800, 300, fill="white", dash=(16, 12), width=2)

        # Ligne d'arret pour les voitures venant de la gauche.
        self.canvas.create_line(320, 250, 320, 350, fill="white", width=3)

        # Ligne d'arret pour les voitures venant de la droite.
        self.canvas.create_line(480, 250, 480, 350, fill="white", width=3)

        # Ligne d'arret pour les voitures venant du haut.
        self.canvas.create_line(350, 220, 450, 220, fill="white", width=3)

        # Ligne d'arret pour les voitures venant du bas.
        self.canvas.create_line(350, 380, 450, 380, fill="white", width=3)
