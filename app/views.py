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
from django.views.decorators.http import require_POST


# Telas de Login e Cadastro #
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

#############################################################


# Tela Home Psico #
@login_required(login_url='/')
@permission_required('admin.psico', login_url='/')
def home_psico(request):
    return render(request, 'home/home_psico.html')

def criar_evento(request):
    criador=request.user
    nomecriador=request.user.first_name
    paciente_id = request.POST['cliente']
    if paciente_id == '':
        paciente = None
        nomepaciente = None
    else:
        paciente = User.objects.get(id=paciente_id)
        nomepaciente= paciente.first_name

    title = request.POST['title']
    description = request.POST['description']
    start = datetime.strptime(request.POST['inicio'], '%Y-%m-%dT%H:%M')
    end = start + timedelta(hours=1)
    end = end.strftime('%Y-%m-%dT%H:%M')
    evento = Events(criador=criador, nomecriador=nomecriador, nomepaciente=nomepaciente, paciente=paciente, title=title, description=description, start=start, end = end)
    evento.save()
    return redirect('home_psico')

def editar_evento(request):
    idev = request.POST['idEditar']
    if idev == '':
        return JsonResponse({'success': False, 'error': 'Evento não encontrado.'})
    else:
        evento = Events.objects.get(id=idev)
        paciente_id = request.POST['editar-cliente']
        if paciente_id == '':
            paciente = None
            nomepaciente = None
        else:
            paciente = User.objects.get(id=paciente_id)
            nomepaciente = paciente.first_name
        
        title = request.POST['editar-title']
        description = request.POST['editar-description']
        start = datetime.strptime(request.POST['editar-inicio'], '%Y-%m-%dT%H:%M')
        end = start + timedelta(hours=1)
        end = end.strftime('%Y-%m-%dT%H:%M')
        evento.paciente = paciente
        evento.nomepaciente = nomepaciente
        evento.title = title
        evento.description = description
        evento.start = start
        evento.end = end
        evento.save()
        return redirect('home_psico')

def excluir_evento(request):
    idev = request.POST['idEvento']
    if idev == '':
        return JsonResponse({'success': False, 'error': 'Evento não encontrado.'})
    else:
        evento = Events.objects.get(id=idev)
        evento.delete()
        return redirect('home_psico')
    
def eventos_json(request):
    eventos = Events.objects.all()
    eventos = eventos.filter(criador=request.user)
    eventos_json = []
    for evento in eventos:
        evento_json = {
            'id': evento.id,
            'title': evento.title,
            'paciente': str(evento.nomepaciente),
            'psico': str(evento.nomecriador),
            'start': evento.start.strftime('%Y-%m-%dT%H:%M'),
            'end': evento.end.strftime('%Y-%m-%dT%H:%M'),
            'descricao': evento.description,
        }
        eventos_json.append(evento_json)
    return JsonResponse(eventos_json, safe=False)

def get_clientes(request):
    clientes = User.objects.filter(user_permissions__codename='cliente')
    return JsonResponse({'clientes': list(clientes.values())})
#############################################################


# Tela Home Cliente #
def home_cliente_load(request):
    eventos = Events.objects.all()
    eventos = eventos.filter(paciente=request.user)
    eventos_cliente_json = []
    for evento in eventos:
        evento_json = {
            'id': evento.id,
            'title': evento.title,
            'paciente': str(evento.nomepaciente),
            'psico': str(evento.nomecriador),
            'start': evento.start.strftime('%Y-%m-%dT%H:%M'),
            'end': evento.end.strftime('%Y-%m-%dT%H:%M'),
            'descricao': evento.description,
        }
        eventos_cliente_json.append(evento_json)
    return JsonResponse(eventos_cliente_json, safe=False)

@login_required(login_url='/')
@permission_required('admin.cliente', login_url='/')
def home_cliente(request):
    return render(request, 'home/home_cliente.html' )

def marcar_evento(request):
    evento_id = request.POST.get('idEvento')
    evento = Events.objects.get(id=evento_id)
    evento.paciente = request.user
    evento.nomepaciente = request.user.first_name
    evento.save()
    return redirect('agendar_cliente')

def get_psicos(request):
    psicos = User.objects.filter(user_permissions__codename='psico')
    return JsonResponse({'psicos': list(psicos.values())})
#############################################################


# Telas Sair e e voltar #
def sair(request):
    logout(request)
    return redirect('/')  
#############################################################


# Tela Agendar Cleinte #
def agendar_cliente_load(request):
    eventos = Events.objects.all()
    eventos = eventos.filter(paciente=None)
    eventos = eventos.filter(criador=request.POST['psico'])
    eventos_cliente = []
    for evento in eventos:
        evento_json = {
            'id': evento.id,
            'title': evento.title,
            'groupId': str(evento.nomepaciente),
            'psico': str(evento.nomecriador),
            'start': evento.start.strftime('%Y-%m-%dT%H:%M'),
            'end': evento.end.strftime('%Y-%m-%dT%H:%M'),
            'descricao': evento.description,
        }
        eventos_cliente.append(evento_json)

    eventos_cliente_json = json.dumps(eventos_cliente)
    context = {
        'eventos_cliente_json': eventos_cliente_json,
    }
    return render(request, 'agendar/agendar_cliente.html', context)

def agendar_cliente(request):
    return render(request, 'agendar/agendar_cliente.html')
#############################################################
