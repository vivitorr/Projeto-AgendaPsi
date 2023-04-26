document.addEventListener('DOMContentLoaded', function() {
  var calendarEl = document.getElementById('calendar');

  var calendar = new FullCalendar.Calendar(calendarEl, {
    initialView: 'dayGridMonth',
    timeZone: 'America/Sao_Paulo',
    locale: 'pt-br',
    selectable: true,
    

    headerToolbar:{
      start: 'dayGridMonth listWeek',
      center: 'title',
      end: 'prev today next'
    },

    buttonText:{
      today:    'hoje',
      month:    'mês',
      week:     'semana',
      day:      'dia',
      list:     'lista'
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