from tfg.models import Mapa,Personaje,equipo,jugador
import csv
import re
import os
from django.conf import settings
CSV_FILE = os.path.join(settings.BASE_DIR, "Database data", "valorant_jugadores.csv")

def run():

    Mapa.objects.update_or_create(nombre="Ascent", defaults={"numero_Iniciadores":2, "numero_Controlador":1, "numero_Centinela":1, "numero_Duelista":1, "imagen_mapa":"imagenes/mapas/Ascent.png"})
    Mapa.objects.update_or_create(nombre="Bind", defaults={"numero_Iniciadores":1, "numero_Controlador":2, "numero_Centinela":0, "numero_Duelista":2, "imagen_mapa":"imagenes/mapas/Bind.png"})
    Mapa.objects.update_or_create(nombre="Split", defaults={"numero_Iniciadores":1, "numero_Controlador":2, "numero_Centinela":1, "numero_Duelista":1, "imagen_mapa":"imagenes/mapas/Split.png"})
    Mapa.objects.update_or_create(nombre="Haven", defaults={"numero_Iniciadores":2, "numero_Controlador":1, "numero_Centinela":1, "numero_Duelista":1, "imagen_mapa":"imagenes/mapas/Haven.png"})
    Mapa.objects.update_or_create(nombre="Icebox", defaults={"numero_Iniciadores":1, "numero_Controlador":1, "numero_Centinela":0, "numero_Duelista":3, "imagen_mapa":"imagenes/mapas/Icebox.png"})
    Mapa.objects.update_or_create(nombre="Breeze", defaults={"numero_Iniciadores":2, "numero_Controlador":1, "numero_Centinela":0, "numero_Duelista":2, "imagen_mapa":"imagenes/mapas/Breeze.png"})
    Mapa.objects.update_or_create(nombre="Fracture", defaults={"numero_Iniciadores":2, "numero_Controlador":2, "numero_Centinela":0, "numero_Duelista":1, "imagen_mapa":"imagenes/mapas/Fracture.png"})
    Mapa.objects.update_or_create(nombre="Pearl", defaults={"numero_Iniciadores":1, "numero_Controlador":1, "numero_Centinela":2, "numero_Duelista":1, "imagen_mapa":"imagenes/mapas/Pearl.png"})
    Mapa.objects.update_or_create(nombre="Lotus", defaults={"numero_Iniciadores":2, "numero_Controlador":2, "numero_Centinela":0, "numero_Duelista":1, "imagen_mapa":"imagenes/mapas/Lotus.png"})
    Mapa.objects.update_or_create(nombre="Sunset", defaults={"numero_Iniciadores":1, "numero_Controlador":1, "numero_Centinela":1, "numero_Duelista":2, "imagen_mapa":"imagenes/mapas/Sunset.png"})
    
   
    Personaje.objects.update_or_create(nombre="Brimstone", defaults={"rol":"Controller", "counter1":"Phoenix", "counter2":"Gekko", "imagen_personaje":"imagenes/agentes/Brimstone.avif"})
    Personaje.objects.update_or_create(nombre="Omen", defaults={"rol":"Controller", "counter1":"Reyna", "counter2":"Raze", "imagen_personaje":"imagenes/agentes/Omen.avif"})
    Personaje.objects.update_or_create(nombre="Viper", defaults={"rol":"Controller", "counter1":"Skye", "counter2":"Jett", "imagen_personaje":"imagenes/agentes/Viper.avif"})
    Personaje.objects.update_or_create(nombre="Astra", defaults={"rol":"Controller", "counter1":"Neon", "counter2":"Phoenix", "imagen_personaje":"imagenes/agentes/Astra.avif"})
    Personaje.objects.update_or_create(nombre="Harbor", defaults={"rol":"Controller", "counter1":"Raze", "counter2":"KAY/O", "imagen_personaje":"imagenes/agentes/Harbor.avif"})
    Personaje.objects.update_or_create(nombre="Clove", defaults={"rol":"Controller", "counter1":"Fade", "counter2":"Sova", "imagen_personaje":"imagenes/agentes/Clove.avif"})
    Personaje.objects.update_or_create(nombre="Jett", defaults={"rol":"Duelist  ", "counter1":"KAY/O", "counter2":"Yoru",   "imagen_personaje":"imagenes/agentes/Jett.avif"})
    Personaje.objects.update_or_create(nombre="Raze", defaults={"rol":"Duelist  ", "counter1":"Cypher", "counter2":"Breach", "imagen_personaje":"imagenes/agentes/Raze.avif"})
    Personaje.objects.update_or_create(nombre="Phoenix", defaults={"rol":"Duelist  ", "counter1":"Viper", "counter2":"Clove", "imagen_personaje":"imagenes/agentes/Phoenix.avif"})
    Personaje.objects.update_or_create(nombre="Reyna", defaults={"rol":"Duelist    ", "counter1":"Iso", "counter2":"Phoenix", "imagen_personaje":"imagenes/agentes/Reyna.avif"})
    Personaje.objects.update_or_create(nombre="Yoru", defaults={"rol":"Duelist    ", "counter1":"Phoenix", "counter2":"Fade", "imagen_personaje":"imagenes/agentes/Yoru.avif"})
    Personaje.objects.update_or_create(nombre="Neon", defaults={"rol":"Duelist    ", "counter1":"Iso", "counter2":"Deadlock", "imagen_personaje":"imagenes/agentes/Neon.avif"})
    Personaje.objects.update_or_create(nombre="Iso", defaults={"rol":"Duelist    ", "counter1":"Harbor", "counter2":"Gekko", "imagen_personaje":"imagenes/agentes/Iso.avif"})
    Personaje.objects.update_or_create(nombre="Sova", defaults={"rol":"Initiator", "counter1":"Killjoy", "counter2":"Breach", "imagen_personaje":"imagenes/agentes/Sova.avif"})
    Personaje.objects.update_or_create(nombre="Skye", defaults={"rol":"Initiator", "counter1":"Fade", "counter2":"Brimstone", "imagen_personaje":"imagenes/agentes/Skye.avif"})
    Personaje.objects.update_or_create(nombre="KAY/O", defaults={"rol":"Initiator", "counter1":"Killjoy", "counter2":"Sova", "imagen_personaje":"imagenes/agentes/Kayo.avif"})
    Personaje.objects.update_or_create(nombre="Breach", defaults={"rol":"Initiator", "counter1":"Deadlock", "counter2":"Viper", "imagen_personaje":"imagenes/agentes/Breach.avif"})
    Personaje.objects.update_or_create(nombre="Fade", defaults={"rol":"Initiator", "counter1":"Killjoy", "counter2":"Deadlock", "imagen_personaje":"imagenes/agentes/Fade.avif"})
    Personaje.objects.update_or_create(nombre="Gekko", defaults={"rol":"Initiator", "counter1":"Iso", "counter2":"Omen", "imagen_personaje":"imagenes/agentes/Gekko.avif"})
    Personaje.objects.update_or_create(nombre="Sage", defaults={"rol":"Sentinel", "counter1":"KAY/O", "counter2":"Omen", "imagen_personaje":"imagenes/agentes/Sage.avif"})
    Personaje.objects.update_or_create(nombre="Cypher", defaults={"rol":"Sentinel", "counter1":"Neon", "counter2":"Harbor", "imagen_personaje":"imagenes/agentes/Cypher.avif"})
    Personaje.objects.update_or_create(nombre="Killjoy", defaults={"rol":"Sentinel", "counter1":"Astra", "counter2":"Sova", "imagen_personaje":"imagenes/agentes/Killjoy.avif"})
    Personaje.objects.update_or_create(nombre="Chamber", defaults={"rol":"Sentinel", "counter1":"Brimstone", "counter2":"Killjoy", "imagen_personaje":"imagenes/agentes/Chamber.avif"})
    Personaje.objects.update_or_create(nombre="Deadlock", defaults={"rol":"Sentinel", "counter1":"Cypher", "counter2":"Brimstone", "imagen_personaje":"imagenes/agentes/Deadlock.avif"})

    equipo.objects.update_or_create(nombre_equipo="Team Heretics", defaults={"jugador1":"benjyfishy", "jugador2":"Wo0t", "jugador3":"MiniBoo", "jugador4":"RieNs", "jugador5":"Boo", "racha":-2,"imagen_equipo":"imagenes/logo equipos/Heretics_logo.png"} )
    equipo.objects.update_or_create(nombre_equipo="Fnatic", defaults={"jugador1":"Alfajer", "jugador2":"Chronicle", "jugador3":"Boaster", "jugador4":"crashies", "jugador5":"kaajak","racha":-1,"imagen_equipo":"imagenes/logo equipos/Fnatic_logo.png"} )
    equipo.objects.update_or_create(nombre_equipo="G2 Esports", defaults={"jugador1":"jawgemo", "jugador2":"valyn", "jugador3":"JonahP", "jugador4":"leaf", "jugador5":"trent","racha":7,"imagen_equipo":"imagenes/logo equipos/G2_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="Team Liquid", defaults={"jugador1":"Keiko", "jugador2":"kamo", "jugador3":"trexx", "jugador4":"nAts", "jugador5":"paTiTek","racha":3,"imagen_equipo":"imagenes/logo equipos/Team_Liquid_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="BBL Esports", defaults={"jugador1":"PROFEK", "jugador2":"LewN", "jugador3":"MAGNUM", "jugador4":"sociablee", "jugador5":"Jamppi","racha":-2,"imagen_equipo":"imagenes/logo equipos/BBL_Esports_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="GIANTX", defaults={"jugador1":"Flickless", "jugador2":"ara", "jugador3":"GRUBINHO", "jugador4":"Cloud", "jugador5":"westside","racha":-1,"imagen_equipo":"imagenes/logo equipos/GIANTX_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="Karmine Corp", defaults={"jugador    1":"pyrolll", "jugador2":"marteen", "jugador3":"Avez", "jugador4":"SUYGETSU", "jugador5":"Saadhak","racha":-1,"imagen_equipo":"imagenes/logo equipos/Karmine_Corp_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="Natus Vincere", defaults={"jugador1":"Ruxic", "jugador2":"hiro", "jugador3":"alexiiik", "jugador4":"ANGE1", "jugador5":"Shao","racha":2,"imagen_equipo":"imagenes/logo equipos/Natus_Vincere_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="Karmine Corp GC", defaults={"jugador1":"Jiex", "jugador2":"alkyia", "jugador3":"Glance", "jugador4":"safiaa", "jugador5":"anesilia","racha":6,"imagen_equipo":"imagenes/logo equipos/Karmine_Corp_logo_fem.png"})
    equipo.objects.update_or_create(nombre_equipo="Gentle Mates", defaults={"jugador1":"Veqaj", "jugador2":"Minny", "jugador3":"kamyk", "jugador4":"ComeBack", "jugador5":"Proxh","racha":-5,"imagen_equipo":"imagenes/logo equipos/Gentle_mates_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="Enterprise Esports", defaults={"jugador1":"starki", "jugador2":"jas", "jugador3":"zeek", "jugador4":"Doma", "jugador5":"Kiles","racha":-1,"imagen_equipo":"imagenes/logo equipos/Enterprise_Esports_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="GIANTX GC", defaults={"jugador1":"Nami", "jugador2":"sarah", "jugador3":"eva", "jugador4":"ness", "jugador5":"Smurfette","racha":0,"imagen_equipo":"imagenes/logo equipos/GIANTX_logo_fem.png"})
    equipo.objects.update_or_create(nombre_equipo="SK Nebula", defaults={"jugador1":"Liza", "jugador2":"Joliinaa", "jugador3":"devilasxa", "jugador4":"jademwah", "jugador5":"PuriTy","racha":0,"imagen_equipo":"imagenes/logo equipos/SK_Nebula_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="BBL PCIFIC", defaults={"jugador1":"Loita", "jugador2":"Crewen", "jugador3":"Rose", "jugador4":"Lar0k", "jugador5":"lovers_rock","racha":0,"imagen_equipo":"imagenes/logo equipos/BBL_PCIFIC_logo.png"})
    equipo.objects.update_or_create(nombre_equipo="ULF Esports", defaults={ "jugador1":"nekky", "jugador2":"Favian", "jugador3":"echo", "jugador4":"audaz", "jugador5":"s0pp","racha":-1,"imagen_equipo":"imagenes/logo equipos/ULF_Esports_logo.png"})    

with open(CSV_FILE, newline='', encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team, _ = equipo.objects.get_or_create(
            nombre_equipo=row["Equipo"],
            defaults={
            "jugador1": "",
            "jugador2": "",
            "jugador3": "",
            "jugador4": "",
            "jugador5": "",
            "racha": 0,
            "imagen_equipo": "imagenes/logo equipos/default.png"
        }
    )           
            jugador.objects.update_or_create(
                nombre_jugador=row["Nombre"],
                equipo= team,
                nacionalidad=row["Nacionalidad"],
                puntuacion=float(row["ACS"]),
                Kills_per_Round=float(row["Kills/Round"]),
                Deaths_per_Round=float(row["Deaths/Round"]),
                Opening_Kills_per_Round=float(row["Open Kills/Round"]),
                Headshot_per_Round=float(row["Headshots/Round"]),
                Kill_Cost=int(float(row["Kill cost"])),
                Mejor_Mapa=re.sub(r"\s*\(.*\)", "", row["Mejor mapa (ACS)"]).strip(),
                Peor_Mapa=re.sub(r"\s*\(.*\)", "", row["Peor mapa (ACS)"]).strip(),
                Rol_Recomendado=row["Rol recomendado"],
                
            )

run()