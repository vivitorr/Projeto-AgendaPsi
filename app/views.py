from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Events
import json
from django.http import JsonResponse
from django.contrib import auth
from datetime import datetime, timedelta
# Create your views here.


def tela_login(request):
    return render(request, 'login_cadastro\login.html')

def loginbanc(request):
    data = {}
    user = authenticate(username= request.POST['user'], password= request.POST['password'])
    if user is not None:
        if User.get_user_permissions(user, obj=None) == {'admin.cliente'}:
                login(request, user)
                return redirect ('/home_cliente/')
        if User.get_user_permissions(user, obj=None) == {'admin.psico'}:
                login(request, user)
                return redirect ('/home_psico/')
    else:
        data ['alert_usuario_ou_senha_incorreta'] = 'não'
        return render(request, 'login_cadastro\login.html', data)

def tela_cadastro(request):
    return render(request, 'login_cadastro\cadastro.html')

def cadastrobanc(request):
    data = {}
    if(request.POST['password'] != request.POST['password-conf']):
        data ['alert_senha_nao_corresponde'] = 'não'
        return render(request, 'login_cadastro\cadastro.html',data)
    else:
        user = User.objects.create_user(request.POST['user'], request.POST['email'], request.POST['password'])
        user.first_name = request.POST['name']
        user.save()
        if (request.POST['perm'] == 'psico'):
            user.user_permissions.add(25)
        else:
            user.user_permissions.add(26)
    data['alert_conta_criada'] = 'sim'
    return render(request, 'login_cadastro\login.html',data)

@login_required(login_url='/')
@permission_required('admin.cliente', login_url='/')
def home_cliente(request):
    return render(request, 'home/home_cliente.html' )
    
@login_required(login_url='/')
@permission_required('admin.psico', login_url='/')
def home_psico(request):
    return render(request, 'home/home_psico.html')

def sair(request):
    logout(request)
    return redirect('/')  

def eventos_json(request):
    eventos = Events.objects.all()
    eventos = eventos.filter(criador=request.user)
    eventos_json = []
    for evento in eventos:
        evento_json = {
            'id': evento.id,
            'title': evento.title,
            'start': evento.start.strftime('%Y-%m-%dT%H:%M:%S'),
            'end': evento.end.strftime('%Y-%m-%dT%H:%M:%S'),
            'descricao': evento.description,
        }
        eventos_json.append(evento_json)
    return JsonResponse(eventos_json, safe=False)


def criar_evento(request):
    criador=request.user
    paciente_id = request.POST['cliente']
    if paciente_id == '':
        paciente = None
    else:
        paciente = User.objects.get(id=paciente_id)

    if paciente == None:
        nomenotitle = 'Disponivel'
    else:
        nomenotitle = paciente.first_name
    title = f"{request.POST['title']} - Paciente: {nomenotitle} - Descrição: {request.POST['description']} "
    description = request.POST['description']
    start = datetime.strptime(request.POST['inicio'], '%Y-%m-%dT%H:%M')
    end = start + timedelta(hours=1)
    end = end.strftime('%Y-%m-%d %H:%M:%S')
    evento = Events(criador=criador, paciente=paciente, title=title, description=description, start=start, end = end)
    evento.save()
    return redirect('home_psico')

def get_clientes(request):
    clientes = User.objects.filter(user_permissions__codename='cliente')
    permissions = Permission.objects.filter(codename='cliente')
    return JsonResponse({'clientes': list(clientes.values()), 'permissions': list(permissions.values())})

