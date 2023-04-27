document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    themeSystem: 'bootstrap5',
    initialView: 'listWeek',
    timeZone: 'America/Sao_Paulo',
    locale: 'pt-br',
    selectable: true,

    headerToolbar:{
      start: 'listWeek,dayGridMonth myCustomButton',
      center: 'title',
      end: 'prev today next'
    },

    customButtons: {
      myCustomButton: {
        text: 'Adicionar Horário',
        click: function() {
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

    events: eventosJsonUrl

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