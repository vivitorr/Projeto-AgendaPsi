document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'listWeek',
    timeZone: 'America/Sao_Paulo',
    locale: 'pt-br',
    selectable: true,
    events: eventosJsonUrl,

    headerToolbar:{
      start: 'listWeek,dayGridMonth myCustomButton',
      center: 'title',
      end: 'prev today next'
    },

    eventTimeFormat: { // like '14:30:00'
      hour: '2-digit',
      minute: '2-digit',
    },

    customButtons: {
      myCustomButton: {
        text: 'Marcar Consulta',
        click: function() {
          fetch('/get_psicos/')
          .then(response => response.json())
          .then(data => {
            const select = document.getElementById('psico');
            select.innerHTML = '<option value=""selected>Todos</option>';
            data.psicos.forEach(psicos => {
              const option = document.createElement('option');
              option.text = psicos.first_name;
              option.value = psicos.username;
              select.add(option);
            });
          });
          document.getElementById("modal-escolher-psico").style.display = "block";
        }
      }
    },

    buttonText:{
      today:    'Hoje',
      month:    'Calendario',
      week:     'semana',
      day:      'dia',
      list:     'Agenda'
    },

    dateClick: function(info) {
      if(info.view.type == 'dayGridMonth'){
        calendar.changeView('timeGrid', info.dateStr);
      }
    },

    eventClick: function(info) {
      var evento = info.event;
      var idEvento = evento.id;
      
      // Exibir a modal
      document.getElementById('modal-evento').style.display = 'block';

      // Preencher os campos do modal com as informações do evento clicado
      document.getElementById('tituloEvento').innerHTML = evento.title;
      document.getElementById('pacienteEvento').innerHTML = evento.extendedProps.paciente === 'None' ? 'Disponível' : evento.extendedProps.paciente;
      document.getElementById('descricaoEvento').innerHTML = evento.extendedProps.descricao ? evento.extendedProps.descricao : 'Sem descrição';
      document.getElementById('dataInicioEvento').innerHTML = evento.start.toLocaleDateString('pt-BR', {timeZone: 'UTC'}) + ' ' + evento.start.toLocaleTimeString('pt-BR', 
      {timeZone: 'UTC'});
      document.getElementById('idEvento').value = idEvento;
  
  
  },

  });
  calendar.render();

});

document.getElementById("modal-escolher-psico").addEventListener("click", function(event) {
  if (event.target == document.getElementById("modal-escolher-psico")) {
    document.getElementById("modal-escolher-psico").style.display = "none";
  }
});

document.getElementById("modal-evento").addEventListener("click", function(event) {
    if (event.target == document.getElementById("modal-evento")) {
      document.getElementById("modal-evento").style.display = "none";
    }
});

function getCSRFToken() {
  const cookieValue = document.cookie
    .split("; ")
    .find(row => row.startsWith("csrftoken="));

  if (cookieValue) {
    return cookieValue.split("=")[1];
  }

  return null;
}

// Exibe o modal com o id "modal-noti"
document.getElementById("noti").addEventListener("click", function() {
  fetch("/get_notificacoes/")
    .then(response => response.json())
    .then(notificacoes => {
      var modalBody = document.getElementById("tela-noti");
      modalBody.innerHTML = "<h2>Notificações</h2>";
      for (var i = 0; i < notificacoes.length; i++) {
        var notificacao = notificacoes[i];
        var notificacaoHTML = "<div id='notificacao' class='notificacao'>" + "<div id='tela-fechar' class='tela-fechar'>" + "<button class='btn btn-fechar' data-id='" + notificacao.id + "'>" + "</button>" + "</div>" + "<div id='notificacao' class='notificacao'>" + "<p class='" + (notificacao.visualizado? "" : "conteudo") + "'>" + notificacao.mensagem + "<br>" + "<br>para a data " + notificacao.data + "<br>" + "<br>com " + notificacao.criou + "</p>" + "</div>";

        modalBody.innerHTML += notificacaoHTML;
      }
      var fecharButtons = document.getElementsByClassName("btn-fechar");
      for (var j = 0; j < fecharButtons.length; j++) {
        fecharButtons[j].addEventListener("click", function(event) {
          var notificacao = event.target.closest(".notificacao");
          var idnoti = parseInt(event.target.getAttribute("data-id")); // Converter para inteiro
          console.log("ID da notificação:", idnoti); // Log de depuração
          notificacao.remove();
          
          // Enviar solicitação AJAX para excluir a notificação
          fetch("/excluir_notificacoes/", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": getCSRFToken() // Certifique-se de definir a função getCSRFToken() para obter o token CSRF correto
            },
            body: JSON.stringify({ idnoti: idnoti })
          })
          .then(response => response.json())
          .then(data => {
            console.log("Resposta da exclusão:", data); // Log de depuração
            // Verificar a resposta e realizar ações adequadas, se necessário
          })
          .catch(error => {
            console.error("Erro na exclusão:", error); // Log de depuração
            // Lidar com erros, se necessário
          });
        });
      }
      document.getElementById("modal-noti").style.display = "block";
  })
});

// Quando o usuário clicar em qualquer lugar fora do modal, fechar o modal
document.getElementById("modal-noti").addEventListener("click", function(event) {
  if (event.target == document.getElementById("modal-noti")) {
    document.getElementById("modal-noti").style.display = "none";
  }
});