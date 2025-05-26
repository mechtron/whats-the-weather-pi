# whats-the-weather-pi

Maeve's Sound Box - a special sound box for a special 4-year-old that announces the day and weather when a button is pressed.

This program:
1. Monitors a GPIO button press
1. Gets the current day of the week
1. Fetches current weather data from WeatherAPI.com
1. Uses Gemini to convert text-to-speech and play a personalized message for Maevey

## Feature ideas
1. Cache pre-generated messages

## Hardware requirements:
- Raspberry Pi Zero 2 (or better)
- Button connected to GPIO 12
- Speaker connected to audio output

## Running on Raspberry Pi

### Hardware setup

#### BOM

1. [Raspberry Pi Zero 2 WH](https://www.adafruit.com/product/6008)
1. [Mini External USB Stereo Speaker](https://www.adafruit.com/product/3369)
1. [Micro USB to USB OTG Cable](https://www.amazon.com/dp/B00N9S9Z0G)
1. [Rugged Metal Pushbutton - 16mm 6V RGB Momentary](https://www.adafruit.com/product/3350)
    - [Datasheet](https://cdn-shop.adafruit.com/product-files/3350/Datasheet+.pdf)
1. [5V 2.5A Switching Power Supply with 20AWG MicroUSB Cable](https://www.adafruit.com/product/1995)

#### Setup

1. Use Raspberry Pi Imager to flash your Pi's SD card with Raspberry Pi OS
1. Wire up the RGB pushbutton switch to your Pi
   Pins:
      - Button input: GPIO 12
      - Red LED: GPIO 16
      - Green LED: GPIO 20
      - Blue LED: GPIO 21
1. Plug the speaker into your Pi using the USB to USB OTG cable

### Software setup

1. SSH into your Raspberry Pi: `ssh username@soundbox.local`, where `username` is the user you inputted during setup and `soundbox.local` is your Pi's hostname/IP.
1. Create a new folder `~/soundbox`: `mkdir ~soundbox` and change directories to it: `cd ~/soundbox`
1. Copy the contents of `./src` to your Raspberry Pi: `scp *.* .env username@soundbox.local:/home/username/soundbox`
1. Create a Python virtual environment and activate it: `python3 -m venv venv && source venv/bin/activate`
1. Install Python dependencies: `pip install -r requirements.txt`
1. Set the speaker volume: run `alsamixer` to setup volume (25% is a good starting spot), hit ESC to exit
1. Setup the systemd file:
   1. Create the systemd user service directory (if it doesn't exist): `mkdir -p ~/.config/systemd/user/`
   1. Move `soundbox.service` to `~/.config/systemd/user/`: `mv soundbox.service ~/.config/systemd/user/`
   1. Replace `YOUR_USERNAME` with your linux username
   1. Reload the systemd daemon: `systemctl --user daemon-reload`
   1. Enable the service (to start on boot): `systemctl --user enable soundbox.service`
   1. Start the service: `systemctl --user start soundbox.service`
   1. Check the service status: `systemctl --user status soundbox.service`
   1. View logs: `journalctl --user -u soundbox.service -f`

## Running with Docker (experimental)

1. Copy the example environment file:
   ```bash
   cp src/.env.example src/.env
   ```

2. Edit `src/.env` and add your Gemini and WeatherAPI.com API keys

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
