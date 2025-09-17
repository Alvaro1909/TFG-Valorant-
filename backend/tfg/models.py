from django.db import models

class Mapa(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    numero_Iniciadores = models.IntegerField()
    numero_Controlador = models.IntegerField()
    numero_Centinela = models.IntegerField()
    numero_Duelista = models.IntegerField()
    imagen_mapa = models.ImageField(upload_to='imagenes/mapas',max_length=200)

    def __str__(self):
        return self.nombre

class Personaje(models.Model):
    id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    rol = models.CharField(max_length=50)
    counter1 = models.CharField(max_length=100)
    counter2 = models.CharField(max_length=100)
    imagen_personaje = models.ImageField(upload_to='imagenes/agentes',max_length=200, default=None)
    def __str__(self):
        return self.nombre

class equipo(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_equipo = models.CharField(max_length=100)
    jugador1 = models.CharField(max_length=100)
    jugador2 = models.CharField(max_length=100)
    jugador3 = models.CharField(max_length=100)
    jugador4 = models.CharField(max_length=100)
    jugador5 = models.CharField(max_length=100)
    racha = models.IntegerField()
    imagen_equipo = models.ImageField(upload_to='imagenes/logo_equipos/',max_length=200, default=None)
    def __str__(self):
        return self.nombre_equipo

class jugador(models.Model):
    id = models.AutoField(primary_key=True)
    nombre_jugador = models.CharField(max_length=100)
    equipo = models.ForeignKey(equipo, on_delete=models.CASCADE)
    nacionalidad = models.CharField(max_length=100)
    puntuacion = models.FloatField()
    Kills_per_Round = models.FloatField()
    Deaths_per_Round = models.FloatField()
    Opening_Kills_per_Round = models.FloatField()
    Headshot_per_Round = models.FloatField()
    Kill_Cost = models.FloatField()
    Mejor_Mapa = models.CharField(max_length=100)
    Peor_Mapa = models.CharField(max_length=100)
    Rol_Recomendado = models.CharField(max_length=50)
    def __str__(self):
        return self.nombre_jugador