# MTRX2700 Mechatronics 2
# Major Project - Squid Game

## Role allocations:
**Guess the price:** Cameron Dimovski

**Catapult toss:** Arin Adurkar, Eashan Garg

**Mario kart racing:** Thomas Cook, James Cook

## Guess the price
### Requirement Specification: 
### System Design:
### Detailed Design: 
### Instructions for use:  
### Testing:
### Performance:
## Catapult Toss:
### Requirement Specification:

- A game power meter will run back and forth until the user stops it
- Indication by the power meter will determine how far a projectile is tossed by the catapult
- Whoever makes the projecile travel the least distance is eliminated
  
### System Design:
  
- In order to simulate the power meter, the STM board LEDs will cycle back and forth at about 5ms per change.
- When the user button is pressed, the LED pattern stops and the particular number of LEDs that are ON determines the shooting strength
- Shooting strength determines how much the launching springs are pulled by the servo and in turn the projectile will travel a greater distance for more LEDs ON and a smaller distance for less LEDs ON
  
### Detailed Design:

**Components**
-	Mechanical catapult consisting of springs, bolts, hinges, screws and eyebolts, wood and corflute
-	25kg 6.0-7.4V Servo, HF-S2225MG
-	9g 5V Micro servo, SG90
  
**Individual Modules**
-	```Digital I/O```: The functions ```enable_clocks```, ```initialise_board``` and ```enable_button_interrupts``` in this module are used to enable the STM board LEDs and the user button. ```led_increase``` turns on/off consecutive LEDs each time the function is called. It is used in the power meter simulation. ```countLED``` counts the number of LEDs ON in decimal given the current state in binary using the function ```get_LED```. 
-	```Timers```: This module contains the interrupt handlers for ```TIM2``` and ```TIM3``` as well as the function ```enable_interrupt``` to enable timer interrupts. The function ```timer_initialise``` runs a continuous timer given the time in milliseconds and a void callback function. The function ```trigger_oneshot``` runs a oneshot timer given the time in milliseconds and a void callback function.
-	```HAL PWM```: This module is configured to rotate the servo motors to a certain angle using ```TIM2```. The control register ```CCR1``` controls the release mechanism servo while ```CCR2``` controls the spring loading servo
  
**Integrated Main function**
-	First, the required peripherals are initialised in order to use the LEDs and user button
-	Then the continuous timer is run with ```led_increase``` as a callback in order to simulate the power meter
-	Button interrupts are enabled and the program waits for a button press
-	Once the button is pressed, the continuous timer interrupt and button interrupt are disabled
-	The number of LEDs ON are counted
-	HAL is initialised and ```TIM2``` is configured for PWM output
-	The initial position of the servos is loaded to the control registers
-	After a delay of 2s, the release mechanism is locked
-	After another 2s, the load springs are pulled
-	After 2.5s, the release mechanism is opened and the projectile is shot
-	After 2s, the spring returns to its original position and the program is reset for a new player


### Instructions for use:
### Testing: 
### Performance:
## Mario Kart Racing:
### Requirement Specification: 
### System Design:
### Detailed Design:  
### Instructions for use:  
### Testing:
### Performance:

