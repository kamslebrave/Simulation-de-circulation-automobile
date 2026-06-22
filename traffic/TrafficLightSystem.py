# On importe la classe TrafficLight pour typer les feux recus par le systeme.
from traffic.TrafficLight import TrafficLight


# Cette classe gere les quatre feux de circulation du carrefour.
class TrafficLightSystem:
    def __init__(
        self,
        mbFeu: TrafficLight,
        mtFeu: TrafficLight,
        llFeu: TrafficLight,
        lrFeu: TrafficLight,
    ):
        # Feu de la route principale en bas.
        self.mbFeu = mbFeu

        # Feu de la route principale en haut.
        self.mtFeu = mtFeu

        # Feu lateral a gauche.
        self.llFeu = llFeu

        # Feu lateral a droite.
        self.lrFeu = lrFeu

        # Phase actuelle du systeme de feux.
        # Les phases possibles sont :
        # main_green : route principale au vert.
        # main_yellow : route principale au jaune.
        # all_red_before_lateral : tous les feux au rouge avant le lateral.
        # lateral_green : route laterale au vert.
        # lateral_yellow : route laterale au jaune.
        # all_red_before_main : tous les feux au rouge avant le principal.
        self.phase = "main_green"

        # Temps passe dans la phase actuelle.
        self.phaseTime = 0

        # Duree pendant laquelle une route reste au vert.
        self.greenDuration = 5000

        # Duree pendant laquelle une route reste au jaune.
        self.yellowDuration = 1500

        # Duree de securite pendant laquelle tout le monde reste au rouge.
        self.allRedDuration = 1000

        # Initialisation des couleurs de depart.
        self.initializeTrafficLights()

    def drawTrafficLights(self, canvas):
        # Dessin du feu principal du bas.
        self.mbFeu.drawLight(canvas)

        # Dessin du feu principal du haut.
        self.mtFeu.drawLight(canvas)

        # Dessin du feu lateral gauche.
        self.llFeu.drawLight(canvas)

        # Dessin du feu lateral droit.
        self.lrFeu.drawLight(canvas)

    def initializeTrafficLights(self):
        # Au lancement, le trafic principal commence au vert.
        self.authorizeMainTraffic()

    def stopAllTraffic(self, nextPhase):
        # Cette methode applique la regle de securite :
        # avant de donner le vert a l'autre route, tous les feux passent au rouge.
        self.phase = nextPhase

        # Arret des deux feux principaux.
        self.mbFeu.stopLight()
        self.mtFeu.stopLight()

        # Arret des deux feux lateraux.
        self.llFeu.stopLight()
        self.lrFeu.stopLight()

    def authorizeLateralTraffic(self):
        # On indique que la phase courante est le vert lateral.
        self.phase = "lateral_green"

        # Les deux feux principaux passent au rouge.
        self.mbFeu.stopLight()
        self.mtFeu.stopLight()

        # Les deux feux lateraux passent au vert.
        self.llFeu.authorizeLight()
        self.lrFeu.authorizeLight()

    def authorizeMainTraffic(self):
        # On indique que la phase courante est le vert principal.
        self.phase = "main_green"

        # Les deux feux principaux passent au vert.
        self.mbFeu.authorizeLight()
        self.mtFeu.authorizeLight()

        # Les deux feux lateraux passent au rouge.
        self.llFeu.stopLight()
        self.lrFeu.stopLight()

    def cautionMainTraffic(self):
        # On indique que la phase courante est le jaune principal.
        self.phase = "main_yellow"

        # Les deux feux principaux passent au jaune.
        self.mbFeu.cautionLight()
        self.mtFeu.cautionLight()

        # Les feux lateraux restent au rouge.
        self.llFeu.stopLight()
        self.lrFeu.stopLight()

    def cautionLateralTraffic(self):
        # On indique que la phase courante est le jaune lateral.
        self.phase = "lateral_yellow"

        # Les feux principaux restent au rouge.
        self.mbFeu.stopLight()
        self.mtFeu.stopLight()

        # Les feux lateraux passent au jaune.
        self.llFeu.cautionLight()
        self.lrFeu.cautionLight()

    def update(self, elapsedTime):
        # On ajoute le temps ecoule au compteur de phase.
        self.phaseTime += elapsedTime

        # Si le vert principal a dure assez longtemps, on passe au jaune principal.
        if self.phase == "main_green" and self.phaseTime >= self.greenDuration:
            self.phaseTime = 0
            self.cautionMainTraffic()

        # Si le jaune principal est termine, on met d'abord tout le monde au rouge.
        elif self.phase == "main_yellow" and self.phaseTime >= self.yellowDuration:
            self.phaseTime = 0
            self.stopAllTraffic("all_red_before_lateral")

        # Apres le temps de securite rouge, le trafic lateral recoit le vert.
        elif self.phase == "all_red_before_lateral" and self.phaseTime >= self.allRedDuration:
            self.phaseTime = 0
            self.authorizeLateralTraffic()

        # Si le vert lateral a dure assez longtemps, on passe au jaune lateral.
        elif self.phase == "lateral_green" and self.phaseTime >= self.greenDuration:
            self.phaseTime = 0
            self.cautionLateralTraffic()

        # Si le jaune lateral est termine, on met d'abord tout le monde au rouge.
        elif self.phase == "lateral_yellow" and self.phaseTime >= self.yellowDuration:
            self.phaseTime = 0
            self.stopAllTraffic("all_red_before_main")

        # Apres le temps de securite rouge, le trafic principal recoit le vert.
        elif self.phase == "all_red_before_main" and self.phaseTime >= self.allRedDuration:
            self.phaseTime = 0
            self.authorizeMainTraffic()

    def mainTrafficIsAuthorized(self):
        # Le trafic principal est autorise si ses deux feux sont verts.
        return self.mbFeu.isGreen() and self.mtFeu.isGreen()

    def lateralTrafficIsAuthorized(self):
        # Le trafic lateral est autorise si ses deux feux sont verts.
        return self.llFeu.isGreen() and self.lrFeu.isGreen()

    def directionIsAuthorized(self, direction):
        # Les voitures qui vont a droite ou a gauche appartiennent au trafic principal.
        if direction in ("right", "left"):
            return self.mainTrafficIsAuthorized()

        # Les voitures qui montent ou descendent appartiennent au trafic lateral.
        return self.lateralTrafficIsAuthorized()
