const URL = "http://localhost:8000/";

function get_flight_instances_matches(){
    const start = document.getElementById('start').value;
    const destination = document.getElementById('destination').value;
    const go_date = document.getElementById('go_date').value;
    const return_date = document.getElementById('return_date').value;
    
    const url = URL + `flight_instance_matches?starting_location=${start}&destination=${destination}&depart_date=${go_date}&return_date=${return_date}`;
    fetch(url)
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Error:', error));
}