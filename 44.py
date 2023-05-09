from Adafruit_BBIO import ADC, GPIO
import time

# Initialize the accelerometer
ADC.setup()

# Set up the pins for X, Y, and Z outputs
x_pin = "AIN0"
y_pin = "AIN1"
z_pin = "AIN2"

# Loop to continuously read the accelerometer data
while True:
    # Read the accelerometer data
    x = ADC.read(x_pin)
    y = ADC.read(y_pin)
    z = ADC.read(z_pin)

    # Convert the data to G-forces
    x_g = (x - 1.65) * 3.3 / 0.3
    y_g = (y - 1.65) * 3.3 / 0.3
    z_g = (z - 1.65) * 3.3 / 0.3

    # Display the data
    print("X: " + str(x_g) + " Y: " + str(y_g) + " Z: " + str(z_g))

    # Wait for 0.1 seconds before reading again
    time.sleep(0.1)
