# La classe TrafficLight represente un seul feu de circulation.
class TrafficLight:
    # Duree theorique du vert ou du rouge.
    greenOrRedTime = 30

    # Duree theorique du jaune.
    yellowTime = 5

    def __init__(self, x=0, y=0, name=""):
        # Position horizontale du feu sur le canvas.
        self.x = x

        # Position verticale du feu sur le canvas.
        self.y = y

        # Nom du feu pour l'identifier plus facilement.
        self.name = name

        # Couleur courante du feu.
        self.__color = "Red"

        # Canvas Tkinter sur lequel le feu sera dessine.
        self.canvas = None

        # Identifiant de la lampe rouge sur le canvas.
        self.redLight = None

        # Identifiant de la lampe jaune sur le canvas.
        self.yellowLight = None

        # Identifiant de la lampe verte sur le canvas.
        self.greenLight = None

    def getColor(self):
        # Retourne la couleur actuelle du feu.
        return self.__color

    def isGreen(self):
        # Retourne True si le feu est vert.
        return self.__color == "Green"

    def drawLight(self, canvas=None):
        # Si un canvas est donne, on le garde pour dessiner le feu.
        if canvas is not None:
            self.canvas = canvas

        # Si aucun canvas n'existe, on affiche seulement la couleur en console.
        if self.canvas is None:
            print("Couleur du feu :", self.__color)
            return

        # Si le feu n'a pas encore ete dessine, on cree les formes graphiques.
        if self.redLight is None:
            # Dessin du boitier noir du feu.
            self.canvas.create_rectangle(
                self.x - 6,
                self.y - 6,
                self.x + 26,
                self.y + 76,
                fill="#222222",
                outline="#111111",
            )

            # Dessin de la lampe rouge.
            self.redLight = self.canvas.create_oval(
                self.x,
                self.y,
                self.x + 20,
                self.y + 20,
                fill="#550000",
                outline="black",
            )

            # Dessin de la lampe jaune.
            self.yellowLight = self.canvas.create_oval(
                self.x,
                self.y + 25,
                self.x + 20,
                self.y + 45,
                fill="#665500",
                outline="black",
            )

            # Dessin de la lampe verte.
            self.greenLight = self.canvas.create_oval(
                self.x,
                self.y + 50,
                self.x + 20,
                self.y + 70,
                fill="#005500",
                outline="black",
            )

        # Applique les bonnes couleurs apres le dessin.
        self.updateLight()

    def updateLight(self):
        # Si le feu n'est pas encore dessine, il n'y a rien a mettre a jour.
        if self.canvas is None or self.redLight is None:
            return

        # La lampe rouge devient vive seulement si l'etat est Red.
        red = "#ff0000" if self.__color == "Red" else "#550000"

        # La lampe jaune devient vive seulement si l'etat est Yellow.
        yellow = "#ffd400" if self.__color == "Yellow" else "#665500"

        # La lampe verte devient vive seulement si l'etat est Green.
        green = "#00cc44" if self.__color == "Green" else "#005500"

        # Mise a jour de la couleur de la lampe rouge.
        self.canvas.itemconfig(self.redLight, fill=red)

        # Mise a jour de la couleur de la lampe jaune.
        self.canvas.itemconfig(self.yellowLight, fill=yellow)

        # Mise a jour de la couleur de la lampe verte.
        self.canvas.itemconfig(self.greenLight, fill=green)

    def authorizeLight(self):
        # Le feu passe au vert.
        self.__color = "Green"

        # On met l'affichage a jour.
        self.updateLight()

    def stopLight(self):
        # Le feu passe au rouge.
        self.__color = "Red"

        # On met l'affichage a jour.
        self.updateLight()

    def cautionLight(self):
        # Le feu passe au jaune.
        self.__color = "Yellow"

        # On met l'affichage a jour.
        self.updateLight()
