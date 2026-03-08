from django.shortcuts import render
from rest_framework.views import APIView
from django.http import JsonResponse
from .models import Mapa , Personaje, equipo, jugador
from .serializers import MapaSerializer, PersonajeSerializer, EquipoSerializer, JugadorSerializer
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status



class MapaViewSet(viewsets.ModelViewSet):
    queryset = Mapa.objects.all()
    serializer_class = MapaSerializer

class PersonajeViewSet(viewsets.ModelViewSet):
    queryset = Personaje.objects.all()
    serializer_class = PersonajeSerializer

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = equipo.objects.all()
    serializer_class = EquipoSerializer

class JugadorViewSet(viewsets.ModelViewSet):
    queryset = jugador.objects.all()
    serializer_class = JugadorSerializer

class JugadorTeam(APIView):
    def get(self, request, team_id):
        jugadores = jugador.objects.filter(equipo_id=team_id)
        serializer = JugadorSerializer(jugadores, many=True)
        return Response(serializer.data)


class PrediccionesView(APIView):
    def tipo_composicion(self, ataque, defensa):
        if ataque > defensa:
            return 'Agresiva'
        elif ataque < defensa:
            return 'Defensiva'
        else:
            return 'Equilibrada'

    def post(self, request, *args, **kwargs):
        try:
            puntuacion_ataque_1 =0
            puntuacion_defensa_1 =0
            puntuacion_ataque_2 =0
            puntuacion_defensa_2 =0
            puntuacion_equipo1 =0
            puntuacion_equipo2 =0
            porcentaje_victoria_equipo1 =0
            porcentaje_victoria_equipo2 =0
            listajugadores1 = []
            listajugadores2 = []
            data = request.data
            jugadores1 = data.get("jugadores1")
            jugadores2 = data.get("jugadores2")
            equipo1_id = data.get("equipo1")
            equipo2_id = data.get("equipo2")
            mapa = data.get("mapa")
            agentes = data.get("agentes")
            ajustes = data.get("ajustes", {})
            mapa_actual= Mapa.objects.get(nombre=mapa)
            if not all([jugadores1, jugadores2, mapa, agentes]):
                return Response(
                    {"error": "Faltan datos en la solicitud. Se requieren: jugadores1, jugadores2, mapa, agentes."},
                    status= status.HTTP_400_BAD_REQUEST
                )

            mapa_actual = Mapa.objects.get(nombre=mapa)
            equipo1_obj = equipo.objects.get(id=equipo1_id)
            equipo2_obj = equipo.objects.get(id=equipo2_id)

            agentes_dict = {agente['nombre_jugador']: agente['nombre_agente'] for agente in agentes}
            Diccomposicion1 = {
                "Centinela":mapa_actual.numero_Centinela,
                "Duelista": mapa_actual.numero_Duelista,
                "Iniciadores":mapa_actual.numero_Iniciadores,
                "Controlador":mapa_actual.numero_Controlador}
            
            Diccomposicion2 = {
                "Centinela":mapa_actual.numero_Centinela,
                "Duelista": mapa_actual.numero_Duelista,
                "Iniciadores":mapa_actual.numero_Iniciadores,
               "Controlador":mapa_actual.numero_Controlador}

            
            listajugadores1,puntuacion_ataque_1,puntuacion_defensa_1, puntuacion_equipo1= calcular_lista_jugadores(jugadores1, mapa, agentes_dict,Diccomposicion1, puntuacion_ataque_1, puntuacion_defensa_1, listajugadores1,equipo1_obj, ajustes)
            listajugadores2,puntuacion_ataque_2,puntuacion_defensa_2, puntuacion_equipo2= calcular_lista_jugadores(jugadores2, mapa, agentes_dict,Diccomposicion2, puntuacion_ataque_2, puntuacion_defensa_2, listajugadores2,equipo2_obj, ajustes)

            equipo_que_empieza = request.data.get('equipoQueEmpieza')           
            tipo1 = self.tipo_composicion(puntuacion_ataque_1, puntuacion_defensa_1)
            tipo2 = self.tipo_composicion(puntuacion_ataque_2, puntuacion_defensa_2)
            porcentaje_victoria_equipo1, porcentaje_victoria_equipo2 = clacular_porcentaje_victoria(puntuacion_equipo1, puntuacion_equipo2,equipo_que_empieza,tipo1,tipo2)
                
            resultado = {
                "equipo1": listajugadores1,
                "equipo2": listajugadores2,
                "puntuacion_equipo1": round(puntuacion_equipo1,2),
                "puntuacion_equipo2": round(puntuacion_equipo2,2),
                "porcentaje_victoria_equipo1": round(porcentaje_victoria_equipo1,2),
                "porcentaje_victoria_equipo2": round(porcentaje_victoria_equipo2,2),
                "tipo_composicion_equipo1": tipo1,
                "tipo_composicion_equipo2": tipo2,
            }
            
            return Response(resultado, status=status.HTTP_200_OK)

        except jugador.DoesNotExist:
            return Response({"error": f"No se encontró un jugador con el nombre proporcionado."}, status=status.HTTP_404_NOT_FOUND)
        except Personaje.DoesNotExist:
            return Response({"error": f"No se encontró un personaje con el nombre proporcionado."}, status=status.HTTP_404_NOT_FOUND)
        
    
def clacular_porcentaje_victoria(puntuacion_equipo1, puntuacion_equipo2,equipo_que_empieza,tipo1,tipo2):
            puntuacion_media = (puntuacion_equipo1 + puntuacion_equipo2)
            porcentaje_victoria_equipo1 = (puntuacion_equipo1 / puntuacion_media) * 100
            porcentaje_victoria_equipo2 = (puntuacion_equipo2 / puntuacion_media) * 100
            bonus_table = {
                ('Agresiva', 'Agresiva'): 2.5,
                ('Agresiva', 'Equilibrada'): 1.25,
                ('Equilibrada', 'Agresiva'): 1.25,
                ('Equilibrada', 'Defensiva'): -1.25,
                ('Defensiva', 'Defensiva'): -2.5,
                ('Defensiva', 'Equilibrada'): -1.25,
            }
            if equipo_que_empieza == 'equipo1':
                bonus = bonus_table.get((tipo1, tipo2), 0)
                porcentaje_victoria_equipo1 += bonus
                porcentaje_victoria_equipo2 -= bonus
            elif equipo_que_empieza == 'equipo2':
                bonus = bonus_table.get((tipo2, tipo1), 0)
                porcentaje_victoria_equipo2 += bonus
                porcentaje_victoria_equipo1 -= bonus
            return porcentaje_victoria_equipo1, porcentaje_victoria_equipo2
    


def calcular_lista_jugadores(jugadores, mapa, agentes_dict,Diccomposicion, puntuacion_ataque, puntuacion_defensa, listajugadores,equipo_obj, ajustes=None):
        if ajustes is None:
            ajustes = {}
        
        listajugadores = []
        puntuacion_ataque =0
        puntuacion_defensa =0
        
        multiplicador_kills = 1 if ajustes.get('Kills por ronda') == 1 else 0
        multiplicador_muertes = 1 if ajustes.get('Muerte por ronda') == 1 else 0
        multiplicador_mejor_mapa = 1 if ajustes.get('Mejor mapa') == 1 else 0
        multiplicador_peor_mapa = 1 if ajustes.get('Peor mapa') == 1 else 0
        multiplicador_rol = 1 if ajustes.get('Rol recomendado') == 1 else 0
        multiplicador_kill_cost = 1 if ajustes.get('Coste de kill') == 1 else 0
        multiplicador_opening_kills = 1 if ajustes.get('Primera kill de la ronda') == 1 else 0
        multiplicador_composicion = 1 if ajustes.get('Composición') == 1 else 0
        multiplicador_racha = 1 if ajustes.get('Racha') == 1 else 0
        
        for jugador_id in jugadores:
            score = 0
            jugador_obj = jugador.objects.get(id=jugador_id)
            nombre_jugador = jugador_obj.nombre_jugador
            agente_seleccionado = agentes_dict.get(nombre_jugador)                
            agente_obj = Personaje.objects.get(nombre=agente_seleccionado)
            
            score += (jugador_obj.puntuacion / 2.5) * 0.5 
            score += jugador_obj.Kills_per_Round * 10 * multiplicador_kills
            score -= jugador_obj.Deaths_per_Round * 10 * multiplicador_muertes
            
            best_map = Mapa.objects.get(nombre=jugador_obj.Mejor_Mapa)
            worst_map = Mapa.objects.get(nombre=jugador_obj.Peor_Mapa)
            rol_recomendado = jugador_obj.Rol_Recomendado

            if agente_obj.rol.strip() == rol_recomendado.strip():
                score += 10 * multiplicador_rol

            if best_map.nombre == mapa:
                score += 10 * multiplicador_mejor_mapa
            elif worst_map.nombre == mapa:
                score -= 10 * multiplicador_peor_mapa
                
            score += jugador_obj.Opening_Kills_per_Round * 10 * multiplicador_opening_kills
            score += (jugador_obj.Kill_Cost - 4000) / 100 * multiplicador_kill_cost
            
            for r in Diccomposicion:
                if agente_obj.rol == r:
                    Diccomposicion[r]-=1
                if agente_obj.rol.strip() == "Duelist":
                    puntuacion_ataque +=1
                elif agente_obj.rol.strip() == "Controller":
                    puntuacion_defensa += 1
                elif agente_obj.rol.strip() == "Initiator":
                    puntuacion_ataque += 2
                elif agente_obj.rol.strip() == "Sentinel":
                        puntuacion_defensa += 2
            listajugadores.append({"nombre": nombre_jugador, "score": round(score, 2)})
            
        puntuacion_equipo = sum(jugador['score'] for jugador in listajugadores)/5
                
        if all(value == 0 for value in Diccomposicion.values()):
                    puntuacion_equipo += 15 * multiplicador_composicion
        puntuacion_equipo+= equipo_obj.racha * 2 * multiplicador_racha

        return listajugadores, puntuacion_ataque, puntuacion_defensa,puntuacion_equipo
