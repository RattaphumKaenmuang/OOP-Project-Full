const api = "http://127.0.0.1:8000";

async function search_flight() {
      try {
            const fromSelect = document.getElementById("from_select");
            const toSelect = document.getElementById("to_select");
            const input_from = fromSelect.options[fromSelect.selectedIndex].textContent;
            const input_to = toSelect.options[toSelect.selectedIndex].textContent;
            const input_depart_date = document.getElementById("departure_date").value;
            const input_return_date = document.getElementById("return_date").value;
            const passenger_num = document.getElementById("passenger_num").value;

            localStorage.setItem('input_from', JSON.stringify(input_from));
            localStorage.setItem('input_to', JSON.stringify(input_to));
            localStorage.setItem('input_depart_date', JSON.stringify(input_depart_date));
            localStorage.setItem('input_return_date', JSON.stringify(input_return_date));
            localStorage.setItem('passenger_num', JSON.stringify(passenger_num));
    
            document.location.href = "select_flight.html";

            url = api + "/flight_instance_matches?from=" + input_from + "&to=" + input_to + "&depart_date=" + input_depart_date + "&return_date=" + input_return_date;
            console_log(url);
            fetch(url, {
                  method: 'GET',
                  headers: {
                        'Content-Type': 'application/json',
                  },
            })
            .then(response => response.json())
            .then(data => console.log(data))
      } catch (error) {
          console.error('Error:', error);
      }
}
  
