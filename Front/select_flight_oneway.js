const api = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    const from = JSON.parse(localStorage.getItem('from'));
    const to = JSON.parse(localStorage.getItem('to'));
    const date = JSON.parse(localStorage.getItem('date'));
    const passenger_num = JSON.parse(localStorage.getItem('passenger_num'));

    console.log(from)
    console.log(to)
    console.log(date)
    console.log(passenger_num)


    get_all_flight(from, to, date);
   
});

async function get_all_flight(from, to, date) {
      
      try {
            const response = await fetch(`${api}/flight_instance_matches?starting_location=${from}&destination=${to}&depart_date=${date}&return_date=""`);
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            const response_data = await response.json();
            const parsed_data = await JSON.parse(response_data);
            console.log(parsed_data)

            const departFlights = parsed_data[0];
            //const len_response = departFlights.length;

            const departLabelContainer = document.querySelector(".depart-label");
            departLabelContainer.textContent = `Departure : ${from} --> ${to}`;

            const container = document.getElementById("flight-detail-each-item");

            departFlights.forEach((data,index) => {
                const element = document.createElement("div");
                element.innerHTML = `
                    
                    <label for="depart-time" class="depart-time-label flight-detail-items-i" id="depart-time">${data["departure_time"]}</label>
                    <label for="arrive-time" class="arrive-time-label flight-detail-items-i" id="arrive-time">${data["arrival_time"]}</label>
                    <label for="flight-number" class="flight-number-label flight-detail-items-i" id="flight_number">${data["flight_number"]}</label>
                    <label for="aircraft_number" class="aircraft_number-label flight-detail-items-i" id="aircraft_number">${data["aircraft_number"]}</label>
                    
                    <input type="radio" class="btn-check" name="btnradio" id="btnradio${index}" autocomplete="off" checked>
                    <label class="btn btn-outline-primary" for="btnradio${index}">${data["cost"]}</label>
                    
                `;
                container.appendChild(element);
            });

        } catch (error) {
            console.error('Error:', error);
        }

}

//<input type="radio" class="btn btn-success choose-flight-btn flight-detail-items-i" id="select-btn${index}" name="flightSelection" value="${data["depart_cost"]} Baht">
//<button class="btn btn-success choose-flight-btn flight-detail-items-i" id="select-btn">${data["depart_cost"]} Baht</button>

//<input type="radio" class="btn-check" name="btnradio" id="btnradio${index}" autocomplete="off" checked>
//<label class="btn btn-outline-primary" for="btnradio${index}">${data["depart_cost"]}</label>

