# On importe random pour donner des caracteristiques aleatoires aux voitures.
import random


# La classe Car represente une voiture dans la simulation.
class Car:
    def __init__(
        self,
        color=None,
        width=24,
        height=14,
        speed=None,
        crossRoadChangeDirection=None,
        direction="right",
        x=0,
        y=0,
        canvas=None,
    ):
        # Si aucune couleur n'est donnee, on choisit une couleur au hasard.
        self.color = color or random.choice(["red", "blue", "green", "yellow", "black"])

        # Largeur de la voiture.
        self.width = width

        # Hauteur de la voiture.
        self.height = height

        # Si aucune vitesse n'est donnee, on choisit une vitesse entre 3 et 6 pixels.
        self.speed = speed if speed is not None else random.randint(3, 6)

        # Direction possible au carrefour : tout droit, gauche ou droite.
        self.crossRoadChangeDirection = crossRoadChangeDirection or random.choice(
            ["straight", "left", "right"]
        )

        # Direction de deplacement sur l'ecran : right, left, up ou down.
        self.direction = direction

        # Position horizontale de la voiture.
        self.x = x

        # Position verticale de la voiture.
        self.y = y

        # Canvas Tkinter sur lequel la voiture sera dessinee.
        self.canvas = canvas

        # Identifiant du rectangle dessine sur le canvas.
        self.shape = None

        # Une voiture verticale doit etre plus haute que large.
        if self.direction in ("up", "down"):
            # On inverse largeur et hauteur pour adapter le dessin.
            self.width, self.height = self.height, self.width

        # Si un canvas est fourni, on dessine directement la voiture.
        if self.canvas is not None:
            self.drawCar()

    def drawCar(self):
        # Creation du rectangle qui represente la voiture.
        self.shape = self.canvas.create_rectangle(
            self.x,
            self.y,
            self.x + self.width,
            self.y + self.height,
            fill=self.color,
            outline="black",
        )

    def removeCar(self):
        # Si la voiture est dessinee, on la supprime du canvas.
        if self.canvas is not None and self.shape is not None:
            self.canvas.delete(self.shape)

        # On remet l'identifiant a None car la voiture n'est plus affichee.
        self.shape = None

    def initializeRandomyCar(self):
        # Nouvelle couleur aleatoire.
        self.color = random.choice(["red", "blue", "green", "yellow", "black"])

        # Nouvelle largeur aleatoire.
        self.width = random.randint(18, 26)

        # Nouvelle hauteur aleatoire.
        self.height = random.randint(10, 16)

        # Nouvelle vitesse aleatoire.
        self.speed = random.randint(3, 6)

        # Nouvelle intention de direction au carrefour.
        self.crossRoadChangeDirection = random.choice(["straight", "left", "right"])

    def printCar(self):
        # Affichage de la couleur dans la console.
        print("Car color:", self.color)

        # Affichage de la largeur dans la console.
        print("Car width:", self.width)

        # Affichage de la hauteur dans la console.
        print("Car height:", self.height)

        # Affichage de la vitesse dans la console.
        print("Car speed:", self.speed)

    def move(self, canMove=True):
        # Si canMove vaut False, la voiture reste immobile.
        if not canMove:
            return

        # Deplacement horizontal initialise a zero.
        dx = 0

        # Deplacement vertical initialise a zero.
        dy = 0

        # Si la voiture va vers la droite, on augmente x.
        if self.direction == "right":
            dx = self.speed

        # Si la voiture va vers la gauche, on diminue x.
        elif self.direction == "left":
            dx = -self.speed

        # Si la voiture monte, on diminue y.
        elif self.direction == "up":
            dy = -self.speed

        # Si la voiture descend, on augmente y.
        elif self.direction == "down":
            dy = self.speed

        # Mise a jour de la position logique horizontale.
        self.x += dx

        # Mise a jour de la position logique verticale.
        self.y += dy

        # Si la voiture est affichee, on deplace aussi son rectangle sur le canvas.
        if self.canvas is not None and self.shape is not None:
            self.canvas.move(self.shape, dx, dy)

    def changeSpeed(self, vitesse):
        # Une vitesse negative est remplacee par zero.
        if vitesse < 0:
            vitesse = 0

        # Mise a jour de la vitesse.
        self.speed = vitesse

    def turn(self, direction):
        # On met la direction en minuscule pour faciliter la comparaison.
        direction = direction.lower()

        # On accepte seulement gauche ou droite.
        if direction in ("left", "right"):
            self.direction = direction

    def changeDirection(self):
        # Retourne l'intention de direction au carrefour.
        return self.crossRoadChangeDirection

    def lidar(self, cars):
        # On parcourt toutes les voitures presentes dans la simulation.
        for car in cars:
            # On ignore la voiture elle-meme.
            if car is self:
                continue

            # Une voiture ne doit freiner que pour un vehicule qui va dans le meme sens.
            if car.direction != self.direction:
                continue

            # Verification si les deux voitures sont sur la meme voie horizontale.
            sameHorizontalLane = self.direction in ("left", "right") and abs(self.y - car.y) < 20

            # Verification si les deux voitures sont sur la meme voie verticale.
            sameVerticalLane = self.direction in ("up", "down") and abs(self.x - car.x) < 20

            # Pour une voiture qui va a droite, seul un vehicule devant elle compte.
            if sameHorizontalLane and self.direction == "right":
                distance = car.x - (self.x + self.width)
                if 0 < distance < 35:
                    return True

            # Pour une voiture qui va a gauche, seul un vehicule devant elle compte.
            if sameHorizontalLane and self.direction == "left":
                distance = self.x - (car.x + car.width)
                if 0 < distance < 35:
                    return True

            # Pour une voiture qui descend, seul un vehicule devant elle compte.
            if sameVerticalLane and self.direction == "down":
                distance = car.y - (self.y + self.height)
                if 0 < distance < 35:
                    return True

            # Pour une voiture qui monte, seul un vehicule devant elle compte.
            if sameVerticalLane and self.direction == "up":
                distance = self.y - (car.y + car.height)
                if 0 < distance < 35:
                    return True

        # Aucun obstacle proche n'a ete detecte.
        return False

    def getBounds(self):
        # Retourne les limites du rectangle de la voiture : gauche, haut, droite, bas.
        return (self.x, self.y, self.x + self.width, self.y + self.height)

    def isHorizontal(self):
        # Une voiture horizontale appartient a la route principale.
        return self.direction in ("right", "left")

    def isVertical(self):
        # Une voiture verticale appartient a la route laterale.
        return self.direction in ("up", "down")

    def isOutOfScreen(self, width, height):
        # Retourne True si la voiture est sortie tres loin a gauche.
        return (
            self.x < -80

            # Ou si elle est sortie tres loin a droite.
            or self.x > width + 80

            # Ou si elle est sortie tres loin en haut.
            or self.y < -80

            # Ou si elle est sortie tres loin en bas.
            or self.y > height + 80
        )
