// const api = "http://127.0.0.1:8000";

// document.addEventListener('DOMContentLoaded', function () {
//     const new_input_from = JSON.parse(localStorage.getItem('input_from'));
//     const new_input_to = JSON.parse(localStorage.getItem('input_to'));
//     const new_input_depart_date = JSON.parse(localStorage.getItem('input_depart_date'));
//     const new_input_return_date = JSON.parse(localStorage.getItem('input_return_date'));

//     show_flight(new_input_from, new_input_to, new_input_depart_date, new_input_return_date);
// });

// async function show_flight(new_input_from, new_input_to, new_input_depart_date, new_input_return_date) {
//     try {
//         const response = await fetch(`${api}/flight_instance_matches?froml=${new_input_from}&to=${new_input_to}&depart_date=${new_input_depart_date}&return_date=${new_input_return_date}`);
//         if (!response.ok) {
//             throw new Error(`HTTP error! Status: ${response.status}`);
//         }
//         const response_data = await response.json();
//         console.log(response_data)
//         const depart_flight_data = response_data[0];
//         const return_flight_data = response_data[1];

//         // Departure flight label
//         const departLabelContainer = document.querySelector(".depart-label");
//         departLabelContainer.textContent = `Departure : ${depart_flight_data[0]["depart_starting_location"]} --> ${depart_flight_data[0]["depart_destination"]}`;


//         // Departure flight details
//         const departContainer = document.getElementById("flight-detail-each-item");
//         depart_flight_data.forEach((data, index) => {
//             const element = document.createElement("div");
//             element.innerHTML = `
//                     <label for="depart-time" class="depart-time-label flight-detail-items-i" id="depart-time">${data["depart_departure_time"]}</label>
//                     <label for="arrive-time" class="arrive-time-label flight-detail-items-i" id="arrive-time">${data["depart_arrival_time"]}</label>
//                     <label for="flight-number" class="flight-number-label flight-detail-items-i" id="flight_number">${data["depart_flight_number"]}</label>
//                     <label for="aircraft_number" class="aircraft_number-label flight-detail-items-i" id="aircraft_number">${data["depart_aircraft_number"]}</label>
//                 <button class="btn btn-success choose-flight-btn flight-detail-items-i" id="select-btn" onclick="test(this)">${data["depart_cost"]} Baht</button>
//                 `;
//             departContainer.appendChild(element);
//         });

//         // Return flight label
//         const return_label = document.querySelector(".return-label");
//         return_label.textContent = `Return : ${return_flight_data[0]["return_starting_location"]} --> ${return_flight_data[0]["return_destination"]}`;

//         // Return flight details
//         const returnContainer = document.getElementById("flight-return-detail-each-item");
//         return_flight_data.forEach((data, index)=> {
//             const element = document.createElement("div");
//             element.innerHTML = `
//                 <label for="depart-time" class="depart-time-label flight-detail-items-i" id="depart-time">${data["return_departure_time"]}</label>
//                 <label for="arrive-time" class="arrive-time-label flight-detail-items-i" id="arrive-time">${data["return_arrival_time"]}</label>
//                 <label for="flight-number" class="flight-number-label flight-detail-items-i" id="flight_number">${data["return_flight_number"]}</label>
//                 <label for="aircraft_number" class="aircraft_number-label flight-detail-items-i" id="aircraft_number">${data["return_aircraft_number"]}</label>
//                 <button class="btn btn-success choose-flight-btn flight-detail-items-i" id="select-btn" onclick="test(this)">${data["return_cost"]} Baht</button>
//             `;
//             returnContainer.appendChild(element);
//         });
//     } catch (error) {
//         console.error('Error:', error);
//     }
// }

const api = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    const new_input_from = JSON.parse(localStorage.getItem('input_from'));
    const new_input_to = JSON.parse(localStorage.getItem('input_to'));
    const new_input_depart_date = JSON.parse(localStorage.getItem('input_depart_date'));
    const new_input_return_date = JSON.parse(localStorage.getItem('input_return_date'));

    show_flight(new_input_from, new_input_to, new_input_depart_date, new_input_return_date);
});

async function show_flight(new_input_from, new_input_to, new_input_depart_date, new_input_return_date) {
    try {
        const response = await fetch(`${api}/flight_instance_matches?starting_location=${new_input_from}&destination=${new_input_to}&depart_date=${new_input_depart_date}&return_date=${new_input_return_date}`);
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }
        const response_data = await response.json();
        console.log(response_data)
        const depart_flight_data = response_data[0];
        const return_flight_data = response_data[1];

        // Departure flight label
        const departLabelContainer = document.querySelector(".depart-label");
        departLabelContainer.textContent = `Departure : ${depart_flight_data[0]["depart_starting_location"]} --> ${depart_flight_data[0]["depart_destination"]}`;

        // Departure flight details
        const departContainer = document.getElementById("flight-detail-each-item");
        departContainer.innerHTML = ''; // Clear previous content
        depart_flight_data.forEach((data, index) => {
            const element = document.createElement("div");
            element.innerHTML = `
                    <label for="depart-time" class="depart-time-label flight-detail-items-i" id="depart-time">${data["depart_departure_time"]}</label>
                    <label for="arrive-time" class="arrive-time-label flight-detail-items-i" id="arrive-time">${data["depart_arrival_time"]}</label>
                    <label for="flight-number" class="flight-number-label flight-detail-items-i" id="flight_number">${data["depart_flight_number"]}</label>
                    <label for="aircraft_number" class="aircraft_number-label flight-detail-items-i" id="aircraft_number">${data["depart_aircraft_number"]}</label>
                    <button class="btn btn-success choose-flight-btn flight-detail-items-i" id="select-btn" onclick="selectFile('depart', ${index}, this)">${data["depart_cost"]} Baht</button>
                `;
            departContainer.appendChild(element);
        });

        // Return flight label
        const return_label = document.querySelector(".return-label");
        return_label.textContent = `Return : ${return_flight_data[0]["return_starting_location"]} --> ${return_flight_data[0]["return_destination"]}`;

        // Return flight details
        const returnContainer = document.getElementById("flight-return-detail-each-item");
        returnContainer.innerHTML = ''; // Clear previous content
        return_flight_data.forEach((data, index)=> {
            const element = document.createElement("div");
            element.innerHTML = `
                <label for="depart-time" class="depart-time-label flight-detail-items-i" id="depart-time">${data["return_departure_time"]}</label>
                <label for="arrive-time" class="arrive-time-label flight-detail-items-i" id="arrive-time">${data["return_arrival_time"]}</label>
                <label for="flight-number" class="flight-number-label flight-detail-items-i" id="flight_number">${data["return_flight_number"]}</label>
                <label for="aircraft_number" class="aircraft_number-label flight-detail-items-i" id="aircraft_number">${data["return_aircraft_number"]}</label>
                <button class="btn btn-success choose-flight-btn flight-detail-items-i" id="select-btn" onclick="selectFile('return', ${index}, this)">${data["return_cost"]} Baht</button>
            `;
            returnContainer.appendChild(element);
        });
    } catch (error) {
        console.error('Error:', error);
    }
}

let depart_data = [];
let return_data = [];

function selectFile(type, index, button) {
    const flightDetails = {
        departure_time: button.parentNode.querySelector('.depart-time-label').textContent,
        arrival_time: button.parentNode.querySelector('.arrive-time-label').textContent,
        flight_number: button.parentNode.querySelector('.flight-number-label').textContent,
        aircraft_number: button.parentNode.querySelector('.aircraft_number-label').textContent,
        cost: button.textContent.split(' ')[0] // Extracting cost value
    };

    if (type === 'depart') {
        if (depart_data.length > 0) {
            depart_data[0] = flightDetails;
        } else {
            depart_data.push(flightDetails);
        }
    }

    if (type === 'return') {
        if (return_data.length > 0) {
            return_data[0] = flightDetails;
        } else {
            return_data.push(flightDetails);
        }
    }

    const select_data = [...depart_data, ...return_data];

    console.log("Depart : ", depart_data);
    console.log("Return : ", return_data);
    console.log("Selected : ", select_data);

    localStorage.setItem('select_flight', JSON.stringify(select_data));

}

function to_passengers_fill() {

    const select_flight_data = JSON.parse(localStorage.getItem('select_flight'));
    console.log("Select Flight : ", select_flight_data)
    localStorage.setItem('select_flight', JSON.stringify(select_flight_data));

    document.location.href = "fill_passengers_info.html";

}