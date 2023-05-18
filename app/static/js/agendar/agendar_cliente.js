document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');
  console.log(eventosData)

  var calendar = new FullCalendar.Calendar(calendarEl, {
    themeSystem: 'bootstrap5',
    initialView: 'dayGridMonth',
    timeZone: 'America/Sao_Paulo',
    locale: 'pt-br',
    selectable: true,
    events: eventosData,

    headerToolbar:{
      start: 'dayGridMonth',
      center: 'title',
      end: 'prev today next'
    },

    eventTimeFormat: { // like '14:30:00'
      hour: '2-digit',
      minute: '2-digit',
    },

    buttonText:{
      today:    'Hoje',
      month:    'Calendário',
      week:     'Semana',
      day:      'Dia',
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
      console.log(evento)
      
      // Exibir a modal
      document.getElementById('modal-evento').style.display = 'block';

      // Preencher os campos do modal com as informações do evento clicado
      document.getElementById('tituloEvento').innerHTML = evento.title;
      document.getElementById('criadorEvento').innerHTML = evento.extendedProps.psico;
      document.getElementById('dataInicioEvento').innerHTML = evento.start.toLocaleDateString('pt-BR', {timeZone: 'UTC'}) + ' ' + evento.start.toLocaleTimeString('pt-BR', 
      {timeZone: 'UTC'});
      document.getElementById('idEvento').value = idEvento;
  
  
    },

  });
  
  calendar.render();
});

document.getElementById("modal-evento").addEventListener("click", function(event) {
  if (event.target == document.getElementById("modal-evento")) {
    document.getElementById("modal-evento").style.display = "none";
  }
});


