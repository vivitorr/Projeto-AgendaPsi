document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    themeSystem: 'bootstrap5',
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
        text: 'Adicionar Horário',
        click: function() {
          fetch('/get_clientes/')
          .then(response => response.json())
          .then(data => {
              const select = document.getElementById('cliente');
              select.innerHTML = '<option value=""selected>Disponível</option>';
              data.clientes.forEach(cliente => {
                  const option = document.createElement('option');
                  option.text = cliente.first_name;
                  option.value = cliente.id;
                  select.add(option);
              });
          });
          document.getElementById("modal-criar-evento").style.display = "block";
        }
      }
    },

    buttonText:{
      today:    'Hoje',
      month:    'Calenario',
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
      console.log(idEvento)
      
      // Exibir a modal
      document.getElementById('modal-evento').style.display = 'block';

      // Preencher os campos do modal com as informações do evento clicado
      document.getElementById('tituloEvento').innerHTML = evento.title;
      document.getElementById('pacienteEvento').innerHTML = evento.groupId;
      document.getElementById('descricaoEvento').innerHTML = evento.extendedProps.descricao;
      document.getElementById('dataInicioEvento').innerHTML = evento.start.toLocaleDateString('pt-BR', {timeZone: 'UTC'}) + ' ' + evento.start.toLocaleTimeString('pt-BR', 
      {timeZone: 'UTC'});
      document.getElementById('idEvento').value = idEvento;
  
  
  },

  });
  calendar.render();

});

document.getElementById("adicionar-evento").addEventListener("click", function() {
  document.getElementById("modal-criar-evento").style.display = "block";
});

document.getElementById("fechar-modal").addEventListener("click", function() {
  document.getElementById("modal-criar-evento").style.display = "none";
});

document.getElementById("modal-criar-evento").addEventListener("click", function(event) {
  if (event.target == document.getElementById("modal-criar-evento")) {
    document.getElementById("modal-criar-evento").style.display = "none";
  }
});



document.getElementById("fecharModalEvento").addEventListener("click", function() {
  document.getElementById("modal-evento").style.display = "none";
});

document.getElementById("modal-evento").addEventListener("click", function(event) {
  if (event.target == document.getElementById("modal-evento")) {
    document.getElementById("modal-evento").style.display = "none";
  }
});

