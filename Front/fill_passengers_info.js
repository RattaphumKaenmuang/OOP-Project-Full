const api = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    const len_passenger = JSON.parse(localStorage.getItem('passenger_num'));

    to_passengers_fill(len_passenger);
});

async function to_passengers_fill(len_passenger) {
    try {

        const passenger_container = document.getElementById("container");

        for (var i = 1 ; i < len_passenger ; i++) {

            const element = document.createElement("div");
            element.innerHTML = `
            <div class="pass-container">
                <label class="title-label fw-bold">
                    Passenger ${i + 1}
                </label>
                <div class="pass-input">
                    <div class="input-detail">
                        <div class="info-name">
                            <div class="title-passenger">
                                <label class="title-label">Title</label>
                                <select class="form-select title-input" id="title-input">
                                    <option value="Mr.">Mr.</option>
                                    <option value="Mrs.">Mrs.</option>
                                    <option value="Miss">Miss</option>
                                    <option value="Monk">Monk</option>
                                </select>
                            </div>
                            <div class="first-name-passenger">
                                <label class="first-name-label">First name</label>
                                <input type="text" class="form-control first-name" placeholder="Enter first name" id = "passenger-first-name">
                            </div>
                            <div class="middle-name-passenger">
                                <label class="middle-name-label">Middle name</label>
                                <input type="text" class="form-control middle-name" placeholder="Enter middle name" id = "passenger-middle-name">
                            </div>
                            <div class="last-name-passenger">
                                <label class="last-name-label">Last name</label>
                                <input type="text" class="form-control last-name" placeholder="Enter last name" id = "passenger-last-name">
                            </div>
                        </div>
                    <div class="info-birth">
                        <div class="select-birth">
                            <label class="birth-label">Date of Birth</label>
                            <input type="date" id="birth_date" class="form-select birth-passenger"/>
                        </div>
                    </div>  
                </div>
            </div>
                `;
            passenger_container.appendChild(element);
        }
          
    } catch (error) {
          console.error('Error:', error);
    }
}

function to_select_seat() {

    // const select_flight_data = JSON.parse(localStorage.getItem('select_flight'));
    // console.log("Select Flight : ", select_flight_data)
    // localStorage.setItem('select_flight', JSON.stringify(select_flight_data));

    document.location.href = "select_seat.html";

}

// let depart_data = [];
// let return_data = [];

// function selectFile(type, index, button) {
//     const flightDetails = {
//         departure_time: button.parentNode.querySelector('.depart-time-label').textContent,
//         arrival_time: button.parentNode.querySelector('.arrive-time-label').textContent,
//         flight_number: button.parentNode.querySelector('.flight-number-label').textContent,
//         aircraft_number: button.parentNode.querySelector('.aircraft_number-label').textContent,
//         cost: button.textContent.split(' ')[0] // Extracting cost value
//     };

//     if (type === 'depart') {
//         if (depart_data.length > 0) {
//             depart_data[0] = flightDetails;
//         } else {
//             depart_data.push(flightDetails);
//         }
//     }

//     if (type === 'return') {
//         if (return_data.length > 0) {
//             return_data[0] = flightDetails;
//         } else {
//             return_data.push(flightDetails);
//         }
//     }

//     const select_data = [...depart_data, ...return_data];

//     console.log("Depart : ", depart_data);
//     console.log("Return : ", return_data);
//     console.log("Selected : ", select_data);

//     localStorage.setItem('select_flight', JSON.stringify(select_data));

// }

