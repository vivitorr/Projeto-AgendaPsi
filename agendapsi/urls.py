"""
URL configuration for agendapsi project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LoginView, LogoutView
from app.views import tela_login, tela_cadastro, loginbanc, cadastrobanc, home_cliente, home_psico, sair, eventos_json, criar_evento, get_clientes, excluir_evento, agendar_cliente, get_psicos, agendar_cliente_load, marcar_evento, home_cliente_load, editar_evento

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', tela_login),
    path('cadastro/', tela_cadastro),
    path('cadastrobanc/', cadastrobanc),
    path('loginbanc/', loginbanc),
    path('home_cliente/', home_cliente, name='home_cliente'),
    path('home_psico/', home_psico, name='home_psico'),
    path('sair/', sair),
    path('eventos.json', eventos_json, name='eventos_json'),
    path('criar_evento/', criar_evento, name='criar_evento'),
    path('editar_evento/', editar_evento, name='editar_evento'),
    path('marcar_evento/', marcar_evento, name='marcar_evento'),
    path('get_clientes/', get_clientes, name='get_clientes'),
    path('get_psicos/', get_psicos, name='get_psicos'),
    path('excluir_evento/', excluir_evento, name='excluir_evento'),
    path('agendar_cliente/', agendar_cliente, name='agendar_cliente'),
    path('agendar_cliente_load/', agendar_cliente_load, name='agendar_cliente_load'),
    path('home_cliente_load/', home_cliente_load, name='home_cliente_load'),
]
