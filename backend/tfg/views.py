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

    def post(self, request, *args, **kwargs):
        try:
            puntuacion_ataque_1 =0
            puntuacion_defensa_1 =0
            puntuacion_ataque_2 =0
            puntuacion_defensa_2 =0
            puntuacion_equipo1 =0
            puntuacion_equipo2 =0
            data = request.data
            jugadores1 = data.get("jugadores1")
            jugadores2 = data.get("jugadores2")
            equipo1_id = data.get("equipo1")
            equipo2_id = data.get("equipo2")
            mapa = data.get("mapa")
            agentes = data.get("agentes")
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
            listajugadores1 = []
            listajugadores2 = []
            Diccomposicion1 = {"Centinela":mapa_actual.numero_Centinela,
                                 "Duelista": mapa_actual.numero_Duelista,
                                 "Iniciadores":mapa_actual.numero_Iniciadores,
                                 "Controlador":mapa_actual.numero_Controlador}
            
            Diccomposicion2 = {"Centinela":mapa_actual.numero_Centinela,
                                "Duelista": mapa_actual.numero_Duelista,
                               "Iniciadores":mapa_actual.numero_Iniciadores,
                                   "Controlador":mapa_actual.numero_Controlador}

            for jugador_id in jugadores1:
                score = 0
                jugador_obj = jugador.objects.get(id=jugador_id)
                nombre_jugador = jugador_obj.nombre_jugador
                agente_seleccionado = agentes_dict.get(nombre_jugador)

                if not nombre_jugador or not agente_seleccionado:
                    continue

                agente_obj = Personaje.objects.get(nombre=agente_seleccionado)

                score += (jugador_obj.puntuacion / 2.5) * 0.7
                score += jugador_obj.Kills_per_Round * 10
                score -= jugador_obj.Deaths_per_Round * 10

                best_map = Mapa.objects.get(nombre=jugador_obj.Mejor_Mapa)
                worst_map = Mapa.objects.get(nombre=jugador_obj.Peor_Mapa)
                rol_recomendado = jugador_obj.Rol_Recomendado

                if agente_obj.rol.strip() == rol_recomendado.strip():
                    score += 10
                
                if best_map.nombre == mapa:
                    score += 10
                elif worst_map.nombre == mapa:
                    score -= 10
                
                score += jugador_obj.Opening_Kills_per_Round * 10
                score += (jugador_obj.Kill_Cost - 4000) / 100

                for r in Diccomposicion1:
                    if agente_obj.rol == r:
                        Diccomposicion1[r]-=1
                listajugadores1.append({"nombre": nombre_jugador, "score": round(score, 2)})
            

            for jugador_id in jugadores2:
                score = 0
                jugador_obj = jugador.objects.get(id=jugador_id)
                nombre_jugador = jugador_obj.nombre_jugador
                agente_seleccionado = agentes_dict.get(nombre_jugador)

                if not nombre_jugador or not agente_seleccionado:
                    continue

                agente_obj = Personaje.objects.get(nombre=agente_seleccionado)

                score += (jugador_obj.puntuacion / 2.5) * 0.7
                score += jugador_obj.Kills_per_Round * 10
                score -= jugador_obj.Deaths_per_Round * 10

                best_map = Mapa.objects.get(nombre=jugador_obj.Mejor_Mapa)
                worst_map = Mapa.objects.get(nombre=jugador_obj.Peor_Mapa)
                rol_recomendado = jugador_obj.Rol_Recomendado

                if agente_obj.rol.strip() == rol_recomendado.strip():
                    score += 10

                if best_map.nombre == mapa:
                    score += 10
                elif worst_map.nombre == mapa:
                    score -= 10
                
                score += jugador_obj.Opening_Kills_per_Round * 10
                score += (jugador_obj.Kill_Cost - 4000) / 100
                for r in Diccomposicion2:
                    if agente_obj.rol == r:
                        Diccomposicion2[r]-=1
                listajugadores2.append({"nombre": nombre_jugador, "score": round(score, 2)})

            puntuacion_equipo1 = sum(jugador['score'] for jugador in listajugadores1)/5
            puntuacion_equipo2 = sum(jugador['score'] for jugador in listajugadores2)/5
            
            if all(value == 0 for value in Diccomposicion1.values()):
                puntuacion_equipo1 += 15
            if all(value == 0 for value in Diccomposicion2.values()):
                puntuacion_equipo2 += 15
            
            puntuacion_equipo1+= equipo1_obj.racha*2
            puntuacion_equipo2+= equipo2_obj.racha*2
    

            resultado = {
                "equipo1": listajugadores1,
                "equipo2": listajugadores2,
                "puntuacion_equipo1": round(puntuacion_equipo1,2),
                "puntuacion_equipo2": round(puntuacion_equipo2,2),
            }
            
            return Response(resultado, status=status.HTTP_200_OK)

        except jugador.DoesNotExist:
            return Response({"error": f"No se encontró un jugador con el nombre proporcionado."}, status=status.HTTP_404_NOT_FOUND)
        except Personaje.DoesNotExist:
            return Response({"error": f"No se encontró un personaje con el nombre proporcionado."}, status=status.HTTP_404_NOT_FOUND)
        except KeyError as e:
            return Response({"error": f"Falta la clave en los datos de entrada: {e}"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": f"Ocurrió un error inesperado: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)