# whats-the-weather-pi

Maeve's Sound Box - a special sound box for a special 4-year-old that announces the day and weather
when a button is pressed.

This script:
1. Monitors a GPIO button press
1. Gets the current day of the week
1. Fetches current weather data from WeatherAPI.com
1. Uses text-to-speech to create and play a personalized message for Maevey

## Hardware requirements:
- Raspberry Pi (Zero W, 3, or 4)
- Button connected to GPIO 17 (physical pin 11)
- Speaker connected to audio output

## Running with Docker

1. Copy the example environment file:
   ```bash
   cp src/.env.example src/.env
   ```

2. Edit `src/.env` and add your WeatherAPI.com API key

3. Build the Docker image:
   ```bash
   docker build -t whats-the-weather-pi .
   ```

4. Run the container with GPIO access and environment file:
   ```bash
   docker run --privileged \
     -v /dev:/dev \
     --env-file src/.env \
     whats-the-weather-pi
   ```

Note: The `--privileged` flag and `-v /dev:/dev` are required to access the GPIO pins from within the container.
