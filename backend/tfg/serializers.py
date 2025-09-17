from .models import Mapa, Personaje, equipo, jugador
from rest_framework import serializers
class MapaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mapa
        fields = '__all__'

class PersonajeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Personaje
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    class Meta:
        model = equipo  
        fields = '__all__'

class JugadorSerializer(serializers.ModelSerializer):
    class Meta:
        model = jugador
        fields = '__all__'
