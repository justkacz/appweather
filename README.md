The WeatherApp app offers access to the most recent weather information and delivers detailed forecasts for global locations. <br /> It provides the basic weather measures like temperature, pressure or wind speed along with current weather statistics of all the capital cities in Europe. The open VisualCrossing Weather API is used to fetch weather data:
- for European capitals: request to the weather API is sent daily at 1 AM by executing the serverless function triggered by cron-job. Data are then stored in the Postgres database and used to create charts available on the main page (implemented to avoid exceeding the API request limit on a free-hobby plan).
- other locations: data are collected directly from the API without a database, used for locations entered in the search bar other than European capitals.

![Screenshot from 2024-04-07 21-18-17](https://github.com/justkacz/appweather/assets/80923234/083d977d-e61f-4722-99c2-1e20ab0c9dfb)

