import time
import colorsys

import RPi.GPIO as GPIO


RED_PIN = 13
GREEN_PIN = 19
BLUE_PIN = 26

# A higher frequency makes the dimming smoother (less flicker).
# 100 Hz is generally good for LEDs.
PWM_FREQUENCY = 100

# --- Rainbow Animation Settings ---
# How many steps to go through the rainbow (0.0 to 1.0 for hue)
# More steps = smoother transition, but slower cycle if step_delay is fixed.
NUM_RAINBOW_STEPS = 360 # Represents 360 degrees of hue

# Delay between each step in seconds.
# Smaller delay = faster animation.
STEP_DELAY = 0.015 # 15 milliseconds

RAINBOW_ON = False

# --- Setup GPIO ---
GPIO.setmode(GPIO.BCM)

# Set up pins as outputs and initialize PWM objects
# For Common Anode, the LED is ON when the pin is LOW.
# So, initial duty cycle for 'off' is 100 (HIGH).
# And 0 duty cycle means fully ON (LOW).
# We'll invert the duty cycle values when we set them.
GPIO.setup(RED_PIN, GPIO.OUT)
GPIO.setup(GREEN_PIN, GPIO.OUT)
GPIO.setup(BLUE_PIN, GPIO.OUT)

red_pwm = GPIO.PWM(RED_PIN, PWM_FREQUENCY)
green_pwm = GPIO.PWM(GREEN_PIN, PWM_FREQUENCY)
blue_pwm = GPIO.PWM(BLUE_PIN, PWM_FREQUENCY)

# Start PWM with 100% duty cycle (LEDs off for Common Anode)
red_pwm.start(100)
green_pwm.start(100)
blue_pwm.start(100)


def set_color_hsv(hue, saturation, value):
    """
    Converts HSV to RGB and sets the LED color using PWM.
    Hue: 0.0 to 1.0 (representing 0 to 360 degrees)
    Saturation: 0.0 to 1.0 (0 = grayscale, 1 = full color)
    Value: 0.0 to 1.0 (0 = off, 1 = full brightness)
    """
    r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

    # Convert RGB (0.0-1.0) to PWM duty cycle (0-100)
    # For common anode, 0 duty cycle is brightest, 100 is off.
    # So we need to map 0.0-1.0 to 100-0.
    red_duty_cycle = 100 - int(r * 100)
    green_duty_cycle = 100 - int(g * 100)
    blue_duty_cycle = 100 - int(b * 100)

    # Set PWM duty cycles
    red_pwm.ChangeDutyCycle(red_duty_cycle)
    green_pwm.ChangeDutyCycle(green_duty_cycle)
    blue_pwm.ChangeDutyCycle(blue_duty_cycle)


print("Starting alternating rainbow LED animation. Press Ctrl+C to stop.")


def rainbow_on():
    global RAINBOW_ON
    RAINBOW_ON = True
    while RAINBOW_ON:
        for i in range(NUM_RAINBOW_STEPS):
            # Calculate hue as a fraction of 360 degrees
            hue = i / float(NUM_RAINBOW_STEPS)

            # Set color using HSV (Saturation and Value are always 1.0 for pure, bright colors)
            set_color_hsv(hue, 1.0, 1.0)
            time.sleep(STEP_DELAY)


def rainbow_off():
    global RAINBOW_ON
    RAINBOW_ON = False
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
