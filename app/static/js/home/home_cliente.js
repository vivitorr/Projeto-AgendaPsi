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