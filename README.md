# Pi-Proximity
This python script is used with an ultrasonic range sensor, led, and a buzzer in order to create a proximity alarm sensor and logs the date and time that the sensor activated.

#Description:
When an object is less than or equal to 3ft away from the sensor, the buzzer will sound and the LED is high. Otherwise, the buzzer is silent and the LED is low. When the sensor detects, it logs the date and time of the incident in a MySQL database, which should be installed onto your Raspberry Pi.

#Use:
This python script was created for a Raspberry Pi single-board computer and is written in Python 2. It does require the knowledge of building the circuit. Be sure to change the GPIO pins and range distance to your liking. Also, don't forget to install MySql onto your Raspberry Pi and change the connection variables to your own.
