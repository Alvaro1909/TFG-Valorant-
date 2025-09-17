from django.shortcuts import render
from rest_framework.views import APIView

from .models import Mapa , Personaje, equipo, jugador
from .serializers import MapaSerializer, PersonajeSerializer, EquipoSerializer, JugadorSerializer
from rest_framework import viewsets
from rest_framework.response import Response

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
    