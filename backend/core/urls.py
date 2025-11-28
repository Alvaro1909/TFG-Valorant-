"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tfg.views import JugadorTeam, EquipoViewSet, PersonajeViewSet,MapaViewSet, PrediccionesView
from django.conf import settings
from django.views.generic import RedirectView
from django.conf.urls.static import static
equipo_list = EquipoViewSet.as_view({'get': 'list'})
equipo_detail = EquipoViewSet.as_view({'get': 'retrieve'})
agente_list = PersonajeViewSet.as_view({'get': 'list'})
map_list = MapaViewSet.as_view({'get': 'list'})


urlpatterns = [

    path('admin/', admin.site.urls),
    path("api/teams/", equipo_list, name="team-list"),
    path("api/teams/<int:pk>/", equipo_detail, name="team-detail"),
    path("api/teams/<int:team_id>/jugadores/", JugadorTeam.as_view(), name="jugadores-por-team"),
    path('api/agentes/', agente_list, name='agente-list'),
    path('api/maps/', map_list, name='map-list'),
    path("", RedirectView.as_view(url="api/teams") ),
    path('api/predicciones/', PrediccionesView.as_view(), name='predicciones'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

