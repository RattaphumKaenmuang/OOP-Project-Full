const api = "http://127.0.0.1:8000";

document.addEventListener('DOMContentLoaded', function () {
    const booking_ref_data = JSON.parse(localStorage.getItem('booking_ref'));
    const last_name_data = JSON.parse(localStorage.getItem('last_name'));
    const type_data = JSON.parse(localStorage.getItem('type'));
    console.log(booking_ref_data)
    console.log(last_name_data)
    console.log(type_data)
    get_boarding_pass(booking_ref_data, last_name_data, type_data);
});

async function get_boarding_pass(booking_ref, last_name, type) {
    try {
        const response = await fetch(`${api}/boarding_pass?booking_ref=${booking_ref}&last_name=${last_name}&type=${type}`);
        
        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const response_data = await response.json();
        console.log(response_data);

        
            
    } catch (error) {
        console.error('Error:', error);
    }

}
