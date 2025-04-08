document.addEventListener('DOMContentLoaded', () => {
    // Define the API key and get references to necessary DOM elements
    const apiKey = 'bb4305fc9dbe4db6dfd1c6ff550c5599';
    const searchBtn = document.getElementById('searchBtn');
    const cityInput = document.getElementById('cityInput');
    const weatherInfo = document.getElementById('weatherInfo');
    const unitToggleBtn = document.getElementById('unitToggleBtn');
    let isMetric = true; // To track if the unit is metric or imperial
    let selectedDayIndex = null; // Track the selected day for detailed weather

    // Event listener for search button click
    searchBtn.addEventListener('click', () => {
        const city = cityInput.value.trim(); // Get and trim city name
        if (city) {
            fetchWeather(city); // Fetch weather data if city name is entered
        } else {
            weatherInfo.innerHTML = 'Please enter a city name!'; // Error message if city input is empty
            weatherInfo.style.display = 'block';
            weatherInfo.classList.add('error');
        }
    });

    // Event listener for toggling between metric and imperial units
    unitToggleBtn.addEventListener('click', () => {
        isMetric = !isMetric; // Toggle between metric and imperial
        unitToggleBtn.innerText = isMetric ? "Switch to Imperial" : "Switch to Metric"; // Update button text
        const city = cityInput.value.trim();
        if (city) {
            fetchWeather(city); // Fetch weather again with the new unit system
        }
    });

    // Function to fetch weather data from the API
    async function fetchWeather(city) {
        try {
            weatherInfo.style.display = 'block';
            weatherInfo.innerHTML = 'Loading...'; // Show loading message while fetching data
            weatherInfo.classList.remove('error');

            const units = isMetric ? 'metric' : 'imperial'; // Set units based on the selected system
            const response = await fetch(`https://api.openweathermap.org/data/2.5/forecast?q=${city}&appid=${apiKey}&units=${units}`);
            const data = await response.json(); // Parse the response as JSON

            // Check if the city is valid
            if (data.cod !== "200") {
                weatherInfo.innerHTML = 'City not found!'; // Display error if city is not found
                weatherInfo.style.display = 'block';
                weatherInfo.classList.add('error');
                return;
            }
            displayWeather(data); // Call the function to display weather data
        } catch (error) {
            console.error('Error fetching data:', error);
            weatherInfo.innerHTML = 'Error fetching data! Please try again.'; // Show error if API call fails
            weatherInfo.style.display = 'block';
            weatherInfo.classList.add('error');
        }
    }

    // Function to display the weather data
    function displayWeather(data) {
        let forecastHTML = `<h3>${data.city.name}, ${data.city.country}</h3>`; // Display city name and country

        // Adjust the time for the city's time zone
        const timezoneOffset = data.city.timezone;
        const currentTimeUTC = new Date();
        const currentTimeInCity = new Date(currentTimeUTC.getTime() + timezoneOffset * 1000);

        // Format the adjusted time
        let hours = currentTimeInCity.getHours();
        const minutes = currentTimeInCity.getMinutes();
        const ampm = hours >= 12 ? 'PM' : 'AM';
        hours = hours % 12;
        hours = hours ? hours : 12;
        const formattedTime = `${hours}:${minutes < 10 ? '0' + minutes : minutes} ${ampm}`;
        forecastHTML += `<p><strong>Current Time: </strong>${formattedTime}</p>`;

        const current = data.list[0];
        const currentIcon = getIcon(current.weather[0].icon, currentTimeInCity); // Get the correct icon based on day or night
        const currentTemp = Math.trunc(current.main.temp); // Current temperature
        const feelsLike = Math.trunc(current.main.feels_like); // Feels like temperature
        const currentCondition = current.weather[0].main; // Current weather condition
        const currentHumidity = current.main.humidity; // Current humidity
        const currentWindSpeed = isMetric ? (Math.trunc(current.wind.speed * 3.6)) : (Math.trunc(current.wind.speed * 2.23694)); // Convert wind speed based on unit system

        // Display current weather information
        forecastHTML += `
            <div class="current-weather">
                <img src="${currentIcon}" alt="${currentCondition}" />
                <p><strong>Temperature: </strong>${currentTemp}°${isMetric ? 'C' : 'F'}</p>
                <p><strong>Feels Like: </strong>${feelsLike}°${isMetric ? 'C' : 'F'}</p>
                <p><strong>Condition: </strong>${currentCondition}</p>
                <p><strong>Humidity: </strong>${currentHumidity}%</p>
                <p><strong>Wind Speed: </strong>${currentWindSpeed} ${isMetric ? 'km/h' : 'mph'}</p>
            </div>
        `;

        let dailyForecast = '';
        const forecastContainer = document.createElement('div');
        forecastContainer.classList.add('forecast-container');

        const daysForecast = {}; // Store forecast data by day

        // Process hourly data and group it by day
        data.list.forEach(entry => {
            let date = new Date(entry.dt * 1000);
            let day = date.toLocaleString('en', { weekday: 'long' }); // Get the day of the week
            let dayNumber = date.getDate(); // Get the day number of the month
            let dateKey = `${day}-${dayNumber}`;

            // Store the forecast data for each day
            if (!daysForecast[dateKey]) {
                daysForecast[dateKey] = {
                    day: day,
                    dayNumber: dayNumber,
                    high: entry.main.temp,
                    low: entry.main.temp,
                    icon: getIcon(entry.weather[0].icon, date),
                    condition: entry.weather[0].main,
                    hourlyTemps: [entry.main.temp],
                    humidity: entry.main.humidity,
                    windSpeed: entry.wind.speed,
                };
            } else {
                // Update high and low temperatures for the day
                daysForecast[dateKey].hourlyTemps.push(entry.main.temp);
                if (entry.main.temp > daysForecast[dateKey].high) {
                    daysForecast[dateKey].high = entry.main.temp;
                }
                if (entry.main.temp < daysForecast[dateKey].low) {
                    daysForecast[dateKey].low = entry.main.temp;
                }
            }
        });

        // Create forecast elements for each day
        Object.keys(daysForecast).forEach(dayKey => {
            const day = daysForecast[dayKey];
            const tempHigh = Math.trunc(day.high);
            const tempLow = Math.trunc(day.low);
            const icon = day.icon;

            const dayForecast = `
                <div class="forecast-day" data-day="${day.day}" data-index="${day.dayNumber}">
                    <h4>${day.day}</h4>
                    <h4>${day.dayNumber}</h4>
                    <img src="${icon}" alt="weather icon" />
                    <p>${tempHigh}°${isMetric ? 'C' : 'F'} / ${tempLow}°${isMetric ? 'C' : 'F'}</p>
                    <p>${day.condition}</p>
                </div>
            `;
            forecastContainer.innerHTML += dayForecast;
        });

        weatherInfo.innerHTML = forecastHTML; // Add the current weather data to the page
        weatherInfo.appendChild(forecastContainer); // Add the daily forecast to the page

        // Add event listeners to forecast days for selecting a day
        const forecastDays = document.querySelectorAll('.forecast-day');
        forecastDays.forEach(day => {
            day.addEventListener('click', () => {
                forecastDays.forEach(d => d.classList.remove('selected'));
                day.classList.add('selected');
                selectedDayIndex = day.getAttribute('data-index');
                updateCurrentWeather(data, selectedDayIndex, daysForecast);
            });
        });

        // If a day is already selected, highlight it and show detailed weather
        if (selectedDayIndex !== null) {
            const selectedDay = forecastContainer.querySelector(`[data-index="${selectedDayIndex}"]`);
            if (selectedDay) {
                selectedDay.classList.add('selected');
                updateCurrentWeather(data, selectedDayIndex, daysForecast);
            }
        }
    }

    // Function to update the detailed weather based on the selected day
    function updateCurrentWeather(data, index, daysForecast) {
        const selectedDay = Object.values(daysForecast).find(day => day.dayNumber === parseInt(index));
        const selectedIcon = selectedDay.icon;
        const selectedTemp = Math.trunc(selectedDay.hourlyTemps[0]);
        const selectedLow = Math.trunc(selectedDay.low);
        const selectedHigh = Math.trunc(selectedDay.high);
        const selectedCondition = selectedDay.condition;
        const selectedHumidity = selectedDay.humidity;
        const selectedWindSpeed = isMetric
            ? (Math.trunc(selectedDay.windSpeed * 3.6)) // Convert wind speed from m/s to km/h
            : (Math.trunc(selectedDay.windSpeed * 2.23694)); // Convert wind speed from m/s to mph

        const currentWeatherDiv = document.querySelector('.current-weather');
        currentWeatherDiv.innerHTML = `
            <img src="${selectedIcon}" alt="${selectedCondition}" />
            <p><strong>Temperature: </strong>${selectedTemp}°${isMetric ? 'C' : 'F'}</p>
            <p><strong>Low of: </strong>${selectedLow}°${isMetric ? 'C' : 'F'}</p>
            <p><strong>High of: </strong>${selectedHigh}°${isMetric ? 'C' : 'F'}</p>
            <p><strong>Condition: </strong>${selectedCondition}</p>
            <p><strong>Humidity: </strong>${selectedHumidity}%</p>
            <p><strong>Wind Speed: </strong>${selectedWindSpeed} ${isMetric ? 'km/h' : 'mph'}</p>
        `;
    }

    // Function to get the correct icon based on the time of day
    function getIcon(iconCode, cityTime) {
        const currentHour = cityTime.getHours();

        const isDay = currentHour >= 6 && currentHour < 18; // Daytime is between 6 AM and 6 PM

        if (isDay && iconCode.endsWith('n')) {
            iconCode = iconCode.slice(0, -1) + 'd'; // Replace 'n' with 'd' for daytime
        } else if (!isDay && iconCode.endsWith('d')) {
            iconCode = iconCode.slice(0, -1) + 'n'; // Replace 'd' with 'n' for nighttime
        }

        return `https://openweathermap.org/img/wn/${iconCode}.png`; // Return the correct icon URL
    }
});
