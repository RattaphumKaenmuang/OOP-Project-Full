const api = "http://127.0.0.1:8000";

async function click_check_in() {
    try {
          const booking_ref = document.getElementById("booking_ref").value;
          const last_name = document.getElementById("last_name").value;

          localStorage.setItem('booking_ref', JSON.stringify(booking_ref));
          localStorage.setItem('last_name', JSON.stringify(last_name));
      
          document.location.href = "select_ticket.html";

    } catch (error) {
          console.error('Error:', error);
    }
  
}