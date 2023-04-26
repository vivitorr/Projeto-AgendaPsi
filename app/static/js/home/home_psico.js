document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
      initialView: 'listWeek',
      
      locale: 'pt-br',
      buttonText: {
        today:    'hoje',
        month:    'Calendario',
        week:     'semana',
        day:      'dia',
        list:     'Agenda'
      },
      headerToolbar: {
        start: 'dayGridMonth listWeek',
        center: 'title',
        end: 'prev today next'
      },
      dateClick: function(info) {
        if(info.view.type == 'dayGridMonth'){
          calendar.changeView('timeGrid', info.dateStr);
        }
      },
      selectable: true,
      events: [
        { // this object will be "parsed" into an Event Object
          title: 'The Title', // a property!
          start: '2023-04-25', // a property!
          end: '2018-04-26' // a property! ** see important note below about 'end' **
        }
      ],
      
    });
    calendar.render()
  });