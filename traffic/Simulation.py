# On importe random pour choisir aleatoirement la direction des voitures.
import random

# On importe tkinter pour creer l'interface graphique.
import tkinter as tk

# On importe la classe qui dessine les routes.
from traffic.RoadSystem import RoadSystem

# On importe la classe qui represente un feu de circulation.
from traffic.TrafficLight import TrafficLight

# On importe la classe qui gere les quatre feux ensemble.
from traffic.TrafficLightSystem import TrafficLightSystem

# On importe la classe qui represente une voiture.
from traffic.car import Car


# La classe Simulation est la classe principale du projet.
# Elle cree la fenetre, les routes, les feux, les voitures et la boucle de mise a jour.
class Simulation:
    def __init__(self):
        # Largeur de la fenetre graphique.
        self.width = 800

        # Hauteur de la fenetre graphique.
        self.height = 600

        # Temps entre deux mises a jour de l'affichage, en millisecondes.
        self.refreshTime = 50

        # Temps entre deux apparitions de voitures, en millisecondes.
        self.spawnTime = 900

        # Compteur qui mesure le temps passe depuis la derniere voiture creee.
        self.timeSinceLastCar = 0

        # Liste qui contient toutes les voitures actuellement dans la simulation.
        self.cars = []

        # Limites du carrefour central : gauche, haut, droite, bas.
        self.intersection = (350, 250, 450, 350)

        # Creation de la fenetre principale Tkinter.
        self.root = tk.Tk()

        # Titre affiche en haut de la fenetre.
        self.root.title("Traffic System")

        # Creation du canvas : c'est la zone ou on dessine routes, feux et voitures.
        self.canvas = tk.Canvas(
            self.root,
            width=self.width,
            height=self.height,
            bg="#79b96d",
        )

        # Affichage du canvas dans la fenetre.
        self.canvas.pack()

        # Creation et dessin du systeme routier.
        self.roadSystem = RoadSystem(self.canvas)

        # Creation du systeme de feux avec quatre feux places autour du carrefour.
        self.trafficLightSystem = TrafficLightSystem(
            TrafficLight(305, 360, "main_bottom"),
            TrafficLight(475, 170, "main_top"),
            TrafficLight(285, 170, "lateral_left"),
            TrafficLight(495, 360, "lateral_right"),
        )

        # Dessin des quatre feux sur le canvas.
        self.trafficLightSystem.drawTrafficLights(self.canvas)

    def generateRandomly4CarsEachSecondInEachDirection(self, numberOfCars):
        # Cette boucle cree plusieurs voitures au demarrage.
        for _ in range(numberOfCars):
            # A chaque tour, on ajoute une voiture aleatoire.
            self.addRandomCar()

    def addRandomCar(self):
        # Choix aleatoire du cote depuis lequel la voiture arrive.
        direction = random.choice(["right", "left", "up", "down"])

        # Si la voiture va vers la droite, elle commence hors ecran a gauche.
        if direction == "right":
            x, y = -40, 275

        # Si la voiture va vers la gauche, elle commence hors ecran a droite.
        elif direction == "left":
            x, y = self.width + 40, 310

        # Si la voiture descend, elle commence hors ecran en haut.
        elif direction == "down":
            x, y = 375, -40

        # Sinon, elle monte et commence hors ecran en bas.
        else:
            x, y = 412, self.height + 40

        # Avant de creer une voiture, on evite de la faire apparaitre sur une voiture deja la.
        if self.spawnPositionIsBusy(direction, x, y):
            return

        # Creation de la voiture avec sa direction, sa position et le canvas.
        car = Car(direction=direction, x=x, y=y, canvas=self.canvas)

        # Ajout de la voiture dans la liste des voitures a mettre a jour.
        self.cars.append(car)

    def spawnPositionIsBusy(self, direction, x, y):
        # Cette fonction evite de creer deux voitures presque au meme endroit.
        for car in self.cars:
            # On verifie seulement les voitures qui viennent du meme cote.
            if car.direction != direction:
                continue

            # Si la nouvelle voiture serait trop proche d'une voiture existante, on refuse.
            if abs(car.x - x) < 70 and abs(car.y - y) < 70:
                return True

        # Aucun vehicule ne gene l'apparition.
        return False

    def rectanglesTouch(self, firstBounds, secondBounds):
        # Recuperation des limites du premier rectangle.
        firstLeft, firstTop, firstRight, firstBottom = firstBounds

        # Recuperation des limites du deuxieme rectangle.
        secondLeft, secondTop, secondRight, secondBottom = secondBounds

        # Retourne True si les deux rectangles se touchent.
        return not (
            firstRight < secondLeft
            or firstLeft > secondRight
            or firstBottom < secondTop
            or firstTop > secondBottom
        )

    def carIsInIntersection(self, car):
        # Une voiture est dans le carrefour si son rectangle touche la zone centrale.
        return self.rectanglesTouch(car.getBounds(), self.intersection)

    def carIsNearIntersectionEntry(self, car):
        # Cette methode verifie si une voiture est proche d'une ligne d'arret.
        # On l'utilise pour appliquer les priorites seulement pres du carrefour.
        if car.direction == "right":
            return 280 <= car.x + car.width <= 350

        if car.direction == "left":
            return 450 <= car.x <= 520

        if car.direction == "down":
            return 180 <= car.y + car.height <= 250

        if car.direction == "up":
            return 350 <= car.y <= 420

        return False

    def intersectionHasPriorityConflict(self, car):
        # Une voiture deja engagee dans le carrefour a la priorite pour sortir.
        if self.carIsInIntersection(car):
            return False

        # Si la voiture est encore loin, elle peut continuer a approcher normalement.
        if not self.carIsNearIntersectionEntry(car):
            return False

        # Les voitures horizontales ne doivent pas entrer si une verticale est deja engagee.
        for otherCar in self.cars:
            # On ignore la voiture que l'on est en train de verifier.
            if otherCar is car:
                continue

            # On regarde seulement les voitures qui sont deja dans le carrefour.
            if not self.carIsInIntersection(otherCar):
                continue

            # Si les deux voitures ne sont pas sur le meme axe, il y a risque de collision.
            if car.isHorizontal() != otherCar.isHorizontal():
                return True

        # Aucun vehicule prioritaire ne bloque l'entree.
        return False

    def canCarMove(self, car):
        # Si le lidar detecte une voiture trop proche, la voiture doit s'arreter.
        if car.lidar(self.cars):
            return False

        # Si un vehicule de l'autre axe est deja dans le carrefour, on attend.
        if self.intersectionHasPriorityConflict(car):
            return False

        # Si la voiture est deja engagee dans le carrefour, elle continue pour le liberer.
        if self.carIsInIntersection(car):
            return True

        # Une voiture qui va vers la droite approche de la ligne d'arret.
        # Elle avance seulement si le trafic principal est autorise.
        if car.direction == "right" and 285 <= car.x + car.width <= 320:
            return self.trafficLightSystem.directionIsAuthorized(car.direction)

        # Une voiture qui va vers la gauche approche de la ligne d'arret.
        # Elle avance seulement si le trafic principal est autorise.
        if car.direction == "left" and 480 <= car.x <= 520:
            return self.trafficLightSystem.directionIsAuthorized(car.direction)

        # Une voiture qui descend approche de la ligne d'arret.
        # Elle avance seulement si le trafic lateral est autorise.
        if car.direction == "down" and 185 <= car.y + car.height <= 220:
            return self.trafficLightSystem.directionIsAuthorized(car.direction)

        # Une voiture qui monte approche de la ligne d'arret.
        # Elle avance seulement si le trafic lateral est autorise.
        if car.direction == "up" and 380 <= car.y <= 420:
            return self.trafficLightSystem.directionIsAuthorized(car.direction)

        # Si la voiture n'est pas devant une ligne d'arret, elle peut avancer.
        return True

    def updateCars(self):
        # On parcourt une copie de la liste pour pouvoir supprimer des voitures sans erreur.
        for car in self.cars[:]:
            # La voiture avance seulement si canCarMove retourne True.
            car.move(self.canCarMove(car))

            # Si la voiture sort completement de la fenetre, elle est supprimee.
            if car.isOutOfScreen(self.width, self.height):
                # Suppression du dessin de la voiture.
                car.removeCar()

                # Suppression de la voiture dans la liste.
                self.cars.remove(car)

    def update(self):
        # Mise a jour du cycle des feux.
        self.trafficLightSystem.update(self.refreshTime)

        # Ajout du temps ecoule depuis la derniere mise a jour.
        self.timeSinceLastCar += self.refreshTime

        # Si le temps d'apparition est atteint, on cree une nouvelle voiture.
        if self.timeSinceLastCar >= self.spawnTime:
            # Remise a zero du compteur.
            self.timeSinceLastCar = 0

            # Creation d'une nouvelle voiture.
            self.addRandomCar()

        # Mise a jour de toutes les voitures.
        self.updateCars()

        # Tkinter rappelle cette methode apres refreshTime millisecondes.
        self.root.after(self.refreshTime, self.update)

    def run(self):
        # Creation de quelques voitures au lancement pour animer tout de suite la scene.
        self.generateRandomly4CarsEachSecondInEachDirection(4)

        # Lancement de la premiere mise a jour.
        self.update()

        # Lancement de la boucle Tkinter qui garde la fenetre ouverte.
        self.root.mainloop()
