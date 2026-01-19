# whats-the-weather-pi

Maeve's Sound Box - a special sound box for a special 4-year-old that announces the day and weather when a button is pressed.

This program:
1. Monitors a GPIO button press
1. Gets the current day of the week
1. Fetches current weather data from WeatherAPI.com
1. Uses Gemini to convert text-to-speech and play a personalized message for Maevey - now including clothing recommendations!

## Hardware requirements
1. [Raspberry Pi Zero 2 WH](https://www.adafruit.com/product/6008)
1. [Mini External USB Stereo Speaker](https://www.adafruit.com/product/3369)
1. [Micro USB to USB OTG Cable](https://www.amazon.com/dp/B00N9S9Z0G)
1. [5V 2.5A Switching Power Supply with 20AWG MicroUSB Cable](https://www.adafruit.com/product/1995)
1. [Arcade Button - 30mm](https://www.adafruit.com/product/471)
1. [Diffused RGB 10mm LED - Common Anode](https://www.adafruit.com/product/848)
    - [Datasheet](https://cdn-shop.adafruit.com/product-files/848/848_Datasheet.pdf)
1. [1N4148 Signal Diode](https://www.adafruit.com/product/1641)
    - [Datasheet](https://cdn-shop.adafruit.com/datasheets/1N4148.pdf)
1. 3 x 560 ohm 5% resistors

## Running on Raspberry Pi

### Hardware setup

1. Use Raspberry Pi Imager to flash your Pi's SD card with Raspberry Pi OS
1. Wire up the pushbutton switch to your Pi
   Pin: GPIO 21
1. Wire up the RGB LED to your Pi
   Pins:
      - Red LED: GPIO 13. In between the LED red cathode and PWM pin, place a 560 ohm resistor and the 1N4148 diode in series.
      - Green LED: GPIO 19. In between the LED green cathode and PWM pine, place a 560 ohm resistor.
      - Blue LED: GPIO 26. In between the LED blue cathode and PWM pine, place a 560 ohm resistor.
1. Plug the speaker into your Pi using the USB to USB OTG cable

### Software setup

1. SSH into your Raspberry Pi: `ssh username@soundbox.local`, where `username` is the user you inputted during setup and `soundbox.local` is your Pi's hostname/IP.
1. Create a new folder `~/soundbox`: `mkdir ~/soundbox` and change directories to it: `cd ~/soundbox`
1. Copy the contents of `./src` to your Raspberry Pi: `scp *.* .env username@soundbox.local:/home/username/soundbox`
1. Rename `.env.example` to `.env` and add your Gemini and WeatherAPI.com API keys: `mv .env.example .env`
1. Create a Python virtual environment and activate it: `python3 -m venv venv && source venv/bin/activate`
1. Install Python dependencies: `pip install -r requirements.txt`
1. Set the speaker volume: run `alsamixer` to setup volume (25% is a good starting spot), hit ESC to exit
1. Setup the systemd file for the soundbox service:
   1. Create the systemd user service directory (if it doesn't exist): `mkdir -p ~/.config/systemd/user/`
   1. Move `soundbox.service` to `~/.config/systemd/user/`: `mv soundbox.service ~/.config/systemd/user/`
   1. Replace `YOUR_USERNAME` with your linux username
   1. Reload the systemd daemon: `systemctl --user daemon-reload`
   1. Enable the service (to start on boot): `systemctl --user enable soundbox.service`
   1. Start the service: `systemctl --user start soundbox.service`
   1. Check the service status: `systemctl --user status soundbox.service`
   1. View logs: `journalctl --user -u soundbox.service -f`
1. Add crontab configuration for the caching service:
   1. Open crontab: `crontab -e`
   1. Enter the following line: `0 * * * * cd /home/YOUR_USERNAME/soundbox && /home/YOUR_USERNAME/soundbox/venv/bin/python cache.py >> /home/YOUR_USERNAME/soundbox/cache.log 2>&1`
   1. Replace `YOUR_USERNAME` with your linux username
   1. Exit and save

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
