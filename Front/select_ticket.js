
const api = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    const booking_ref_data = JSON.parse(localStorage.getItem('booking_ref'));
    const last_name_data = JSON.parse(localStorage.getItem('last_name'));
    console.log(booking_ref_data,last_name_data)
    handleSelectTicketPageData(booking_ref_data, last_name_data);
});

async function handleSelectTicketPageData(booking_ref_data, last_name_data) {
    try {
        const response = await fetch(`${api}/select_ticket?booking_ref=${booking_ref_data}&last_name=${last_name_data}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const response_data = await response.json();
        console.log(response_data);

        const container = document.getElementById('response-container');

        response_data.forEach(data => {
            const element = document.createElement("div");
            element.innerHTML = `
            <div class="card">
                <div class="title-type">
                    <p class="card-title">${data.type}</p>
                </div>
                <div class="card-info">
                    <p>From : ${data.from}</p>
                    <p>To : ${data.to}</p>
                    <p>Date : ${data.date}</p>
                    <p>Flight Number : ${data["flight number"]}</p>
                    <p>Aircraft : ${data.Aircraft}</p>
                    <p>Depart Time : ${data["depart time"]}</p>
                    <p>Arrival Time : ${data["arrival time"]}</p>
                </div> 
                <div class="get-boarding-btn">
                    <a href="#" class="btn btn-primary boarding-btn" onclick="get_bording_pass('${data["flight number"]}','${data.type}')">Get Boarding Pass</a>
                </div>
            </div>
            `;
            container.appendChild(element);
          });
    } catch (error) {
        console.error('Error:', error);
    }
}

function get_bording_pass(flight_number,type) {
    
      localStorage.setItem('type', JSON.stringify(type));

      document.location.href = "boarding_pass.html";
}