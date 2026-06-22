# Ce fichier transforme le dossier traffic en paquet Python.
# Il permet d'importer plus facilement les classes principales du projet.

# Import de la classe qui represente les voitures.
from traffic.car import Car

# Import de la classe qui dessine les routes.
from traffic.RoadSystem import RoadSystem

# Import de la classe principale qui lance toute la simulation.
from traffic.Simulation import Simulation

# Import de la classe qui represente un feu.
from traffic.TrafficLight import TrafficLight

# Import de la classe qui gere les quatre feux.
from traffic.TrafficLightSystem import TrafficLightSystem

# Liste des elements publics du paquet traffic.
__all__ = [
    "Car",
    "RoadSystem",
    "Simulation",
    "TrafficLight",
    "TrafficLightSystem",
]
