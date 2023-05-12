document.getElementById("escolher-psico").addEventListener("click", function() {
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
    
  });