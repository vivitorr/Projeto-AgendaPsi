document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
      themeSystem: 'bootstrap5',
      initialView: 'dayGridMonth',
      timeZone: 'America/Sao_Paulo',
      locale: 'pt-br',
      selectable: true,
      events: { eventos_cliente_json },
  
      headerToolbar:{
        start: 'dayGridMonth myCustomButton',
        center: 'title',
        end: 'prev today next'
      },
  
      eventTimeFormat: { // like '14:30:00'
        hour: '2-digit',
        minute: '2-digit',
      },
  
      buttonText:{
        today:    'Hoje',
        month:    'Calenario',
        week:     'semana',
        day:      'dia',
        list:     'Agenda'
      },
  
      customButtons: {
        myCustomButton: {
          text: 'Buscar',
          click: function() {
            eventosnone = "{% url 'eventosnone_json' %}";
          }
        }
      },

      dateClick: function(info) {
        if(info.view.type == 'dayGridMonth'){
          calendar.changeView('timeGrid', info.dateStr);
        }
      },
  
    });
    
    calendar.render();
  });



