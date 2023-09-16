var cells = document.querySelectorAll(['.mon', '.tue', '.wed', '.thu', '.fri', '.sat', '.sun']); // Replace with the actual class name

var currentCell = null; // To keep track of the currently clicked cell
// Add a click event listener to each cell
cells.forEach(function(cell) {

cell.addEventListener('click', function() {
    // Revert the color of the previous cell (if any)
    if (currentCell !== null) {
        currentCell.style.backgroundColor = ''; // Revert to default background color
    }

    // Change the color of the clicked cell
    this.style.backgroundColor = '#007BFF'; // Replace with the desired color

    // Update the current cell
    currentCell = this;
    var CurCell_DateValue = currentCell.textContent
    console.log("Дата месяца: " + CurCell_DateValue);

    // Send the clickedId value to the server
    sendDataToServer(CurCell_DateValue);
    });
});

function sendDataToServer(CurCell_DateValue) {
    // Define the URL of your server endpoint
    var serverUrl = 'http://127.0.0.1:8000/api/testing/javascript/'; // Replace with the actual server URL
    console.log(serverUrl);
    // Create a JSON object with the data you want to send
    var data = {
        "DateValue": CurCell_DateValue,
    };
    console.log(data);
    // Send a POST request to the server
    fetch(serverUrl, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)

    })
    .then(response => response.json())
    .then(data => {
        // Handle the response from the server if needed
        console.log('Server response:', data);
    })
    .catch(error => {
        console.error('Error:', error);
    });
}