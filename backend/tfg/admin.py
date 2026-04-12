from django.contrib import admin
from .models import Mapa, Personaje, equipo, jugador


@admin.register(Mapa)
class MapaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'numero_Duelista', 'numero_Iniciadores', 'numero_Controlador', 'numero_Centinela']
    search_fields = ['nombre']
    list_filter = ['nombre']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información del Mapa', {
            'fields': ('nombre', 'imagen_mapa')
        }),
        ('Composición Recomendada', {
            'fields': ('numero_Duelista', 'numero_Iniciadores', 'numero_Controlador', 'numero_Centinela'),
            'description': 'Número de agentes recomendados de cada rol en este mapa'
        }),
    )


@admin.register(Personaje)
class PersonajeAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'rol', 'counter1', 'counter2']
    search_fields = ['nombre', 'rol']
    list_filter = ['rol']
    ordering = ['nombre']
    
    fieldsets = (
        ('Información del Agente', {
            'fields': ('nombre', 'rol', 'imagen_personaje')
        }),
        ('Counters', {
            'fields': ('counter1', 'counter2'),
            'description': 'Agentes que countern a este personaje'
        }),
    )


@admin.register(equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ['nombre_equipo', 'racha', 'lista_jugadores']
    search_fields = ['nombre_equipo']
    list_filter = ['racha']
    ordering = ['-racha']
    
    fieldsets = (
        ('Información del Equipo', {
            'fields': ('nombre_equipo', 'racha', 'imagen_equipo')
        }),
        ('Jugadores', {
            'fields': ('jugador1', 'jugador2', 'jugador3', 'jugador4', 'jugador5'),
            'description': 'Los 5 jugadores principales del equipo'
        }),
    )
    
    def lista_jugadores(self, obj):
        jugadores = [obj.jugador1, obj.jugador2, obj.jugador3, obj.jugador4, obj.jugador5]
        return ' | '.join(filter(None, jugadores))
    lista_jugadores.short_description = 'Alineación'


@admin.register(jugador)
class JugadorAdmin(admin.ModelAdmin):
    list_display = ['nombre_jugador', 'equipo', 'Rol_Recomendado', 'puntuacion', 'nacionalidad']
    search_fields = ['nombre_jugador', 'equipo__nombre_equipo', 'nacionalidad']
    list_filter = ['equipo', 'Rol_Recomendado', 'nacionalidad']
    ordering = ['-puntuacion']
    readonly_fields = ['nombre_jugador']
    
    fieldsets = (
        ('Información Personal', {
            'fields': ('nombre_jugador', 'nacionalidad', 'equipo', 'Rol_Recomendado')
        }),
        ('Estadísticas de Combate', {
            'fields': ('Kills_per_Round', 'Deaths_per_Round', 'Opening_Kills_per_Round', 'Headshot_per_Round', 'Kill_Cost'),
            'description': 'Estadísticas detalladas del jugador en combate'
        }),
        ('Desempeño General', {
            'fields': ('puntuacion', 'Mejor_Mapa', 'Peor_Mapa'),
            'description': 'Puntuación general y mapas favoritos'
        }),
    )
