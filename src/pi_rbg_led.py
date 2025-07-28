import time
import colorsys
import logging
import threading

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
rainbow_thread = None
should_set_colors = True  # Flag to prevent color setting when stopping
thread_stop_requested = False  # Additional flag to stop thread more aggressively

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


def force_led_off():
    """Force all LEDs off by stopping and restarting PWM objects"""
    logging.info("Force stopping all LEDs")
    
    # Stop all PWM objects
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    
    # Set GPIO pins to HIGH (off for common anode)
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
    # Restart PWM objects with 100% duty cycle (off)
    red_pwm.start(100)
    green_pwm.start(100)
    blue_pwm.start(100)
    
    logging.info("PWM objects restarted with LEDs off")


def set_color_hsv(hue, saturation, value):
    """
    Converts HSV to RGB and sets the LED color using PWM.
    Hue: 0.0 to 1.0 (representing 0 to 360 degrees)
    Saturation: 0.0 to 1.0 (0 = grayscale, 1 = full color)
    Value: 0.0 to 1.0 (0 = off, 1 = full brightness)
    """
    global should_set_colors, thread_stop_requested
    if not should_set_colors or thread_stop_requested:
        logging.debug("Skipping color set - stopping in progress")
        return  # Don't set colors if we're stopping
    
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


# print("Starting alternating rainbow LED animation. Press Ctrl+C to stop.")


def rainbow_on():
    logging.info("Starting rainbow LED animation")
    global RAINBOW_ON, rainbow_thread, should_set_colors, thread_stop_requested
    RAINBOW_ON = True
    should_set_colors = True  # Allow color setting when starting
    thread_stop_requested = False  # Allow thread to run
    
    def rainbow_loop():
        global should_set_colors
        while RAINBOW_ON and not thread_stop_requested:
            for i in range(NUM_RAINBOW_STEPS):
                if not RAINBOW_ON or thread_stop_requested:
                    break
                # Calculate hue as a fraction of 360 degrees
                hue = i / float(NUM_RAINBOW_STEPS)

                # Set color using HSV (Saturation and Value are always 1.0 for pure, bright colors)
                set_color_hsv(hue, 1.0, 1.0)
                time.sleep(STEP_DELAY)
            # Check again after completing one full rainbow cycle
            if not RAINBOW_ON or thread_stop_requested:
                break
        logging.info("Rainbow loop ended")
    
    # Start rainbow animation in a separate thread
    rainbow_thread = threading.Thread(target=rainbow_loop, daemon=True)
    rainbow_thread.start()


def rainbow_off():
    logging.info("Stopping rainbow LED animation")
    global RAINBOW_ON, rainbow_thread, should_set_colors, thread_stop_requested
    RAINBOW_ON = False
    should_set_colors = False # Set flag to prevent color setting
    thread_stop_requested = True  # Set flag to stop thread more aggressively
    
    # Immediately turn off all LEDs before waiting for thread
    red_pwm.ChangeDutyCycle(100)
    green_pwm.ChangeDutyCycle(100)
    blue_pwm.ChangeDutyCycle(100)
    
    # Set GPIO pins to HIGH (off for common anode) immediately
    GPIO.output(RED_PIN, GPIO.HIGH)
    GPIO.output(GREEN_PIN, GPIO.HIGH)
    GPIO.output(BLUE_PIN, GPIO.HIGH)
    
    logging.info("LEDs turned off, waiting for thread to finish")
    
    # Wait for the thread to finish if it's running
    if rainbow_thread and rainbow_thread.is_alive():
        rainbow_thread.join(timeout=1.0)  # Wait up to 1 second for thread to finish
        if rainbow_thread.is_alive():
            logging.warning("Thread did not finish within timeout")
    
    # Add a small delay to ensure PWM changes take effect
    time.sleep(0.01)
    
    # Force LED off as a final measure
    force_led_off()
    
    logging.info("Rainbow off complete")


def cleanup():
    """Clean up GPIO and PWM objects when program exits"""
    logging.info("Cleaning up GPIO and PWM objects")
    rainbow_off()  # This will stop the rainbow thread if running
    
    # Stop PWM objects
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    
    # Clean up GPIO
    GPIO.cleanup()
    
    logging.info("GPIO cleanup complete")
