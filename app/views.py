from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound
from django.contrib.auth.models import User, Permission
from django.contrib.auth.decorators import permission_required, login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Events, Notificacoes
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

def criar_notificacao(mensagem, criou, recebeu, data):
    if recebeu == None:
        pass
    else:
        notificacao = Notificacoes(mensagem=mensagem, criou=criou, recebeu=recebeu, data=data)
        notificacao.save()


def criar_evento(request):
    criador = request.user
    nomecriador = request.user.first_name
    paciente_id = request.POST['cliente']
    paciente = User.objects.get(id=paciente_id) if paciente_id else None
    nomepaciente = paciente.first_name if paciente else None
    title = request.POST['title']
    description = request.POST['description']
    start = datetime.strptime(request.POST['inicio'], '%Y-%m-%dT%H:%M')
    end = start + timedelta(hours=1)
    end = end.strftime('%Y-%m-%dT%H:%M')
    evento = Events.objects.create(
        criador=criador,
        nomecriador=nomecriador,
        nomepaciente=nomepaciente,
        paciente=paciente,
        title=title,
        description=description,
        start=start,
        end=end
    )
    criar_notificacao('Novo consulta', criador, paciente, start)
    return redirect('home_psico')

def editar_evento(request):
    evento = get_object_or_404(Events, id=request.POST['idEditar'])
    paciente_id = request.POST['editar-cliente']
    paciente = User.objects.get(id=paciente_id) if paciente_id else None
    nomepaciente = paciente.first_name if paciente else None
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
    criador = request.user
    criar_notificacao('Consulta Editada', criador, paciente, start)
    return redirect('home_psico')

def excluir_evento(request):
    idev = request.POST['idEvento']
    if not request.user.is_authenticated:
        return redirect('tela_login')
    elif User.get_user_permissions(request.user, obj=None) == {'admin.psico'}:
        # código para exclusão do evento
        evento = Events.objects.get(id=idev)
        criador = evento.criador
        paciente = evento.paciente
        start = evento.start
        evento.delete()
        criar_notificacao('Consulta desmarcada', criador, paciente, start)
        return redirect('home_psico')
    elif User.get_user_permissions(request.user, obj=None) == {'admin.cliente'}:
        # código para exclusão do evento
        evento = Events.objects.get(id=idev)
        criador = evento.criador
        paciente = evento.paciente
        start = evento.start
        evento.delete()
        criar_notificacao('Consulta desmarcada', criador, paciente, start)
        return redirect('home_cliente')
    else:
        return HttpResponse('Usuário sem permissão para acessar esta página')

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

def excluir_notificacoes(request):
    data = json.loads(request.body)
    idnoti = data['idnoti']
    print(idnoti)
    notificacao = Notificacoes.objects.get(id=idnoti)
    notificacao.delete()

    return JsonResponse({'status': 'success'})


def get_notificacoes(request):
    notificacoes = Notificacoes.objects.all()
    notificacoes = Notificacoes.objects.filter(recebeu=request.user)
    notificacoes_json = []
    for notificacao in notificacoes:
        notificacao_json = {
            'id': notificacao.id,
            'mensagem': notificacao.mensagem,
            'criou': str(notificacao.criou),
            'data': notificacao.data.strftime('%Y-%m-%d %H:%M:%S'),
            'visualizado': notificacao.visualizado,
        }
        notificacoes_json.append(notificacao_json)
    return JsonResponse(notificacoes_json, safe=False)

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
    criador = request.user
    recebeu = evento.criador
    start = evento.start
    criar_notificacao('Consulta Marcada', criador, recebeu, start)
    return render(request, 'home/home_cliente.html' )

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
