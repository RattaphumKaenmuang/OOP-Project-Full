const api = "http://127.0.0.1:8000";

async function search_flights() {
    try {
          const from = document.getElementById("from_select").value;
          const to = document.getElementById("to_select").value;
          const date = document.getElementById("departure_date").value;
          const passenger_num = document.getElementById("passenger_num").value;

          localStorage.setItem('from', JSON.stringify(from));
          localStorage.setItem('to', JSON.stringify(to));
          localStorage.setItem('date', JSON.stringify(date));
          localStorage.setItem('passenger_num', JSON.stringify(passenger_num));
          
          document.location.href = "select_flight_oneway.html";

    } catch (error) {
          console.error('Error:', error);
    }
  
}