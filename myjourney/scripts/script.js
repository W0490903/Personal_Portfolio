document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM content loaded");

    const mapElement = document.getElementById('map');

    if (mapElement) {
        console.log("Map element found:", mapElement);

        try {
            var map = L.map('map').setView([51.505, -0.09], 13);

            L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            }).addTo(map);

            console.log("Leaflet map initialized successfully.");
        } catch (error) {
            console.error("Leaflet map initialization error:", error);
        }
    } else {
        console.error("Map element with ID 'map' not found.");
    }
    console.log("end of javascript");
});