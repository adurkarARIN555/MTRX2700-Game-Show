# MTRX2700 Mechatronics 2
# Major Project - Squid Game

## Role allocations:
|GAME|Person(s) responsible
|------------|------------------------
|The Price Is Right|Cameron Dimovski
|Catapult Toss|Eashan Garg & Arin Adurkar
|Mario Kart|Thomas Cook & James Cook
## The Price Is Right
### Requirement Specification: 
- The game "The Price Is Right" overall is supposed to function like the TV show. The game is a simplified online version of the game. The user will need an STM32 microcontroller as well as importing the standard definitions folder for the STM32 "stm32f303xc.h". To use the GUI the required libraries QtCore, QtWidgets and QtGui from PyQt5.
- Slider Control: The program allows the two users to control PyQt widget sliders through sliding their fingers over the potentiometer. The current value should be displayed to the screen.
- Timer Control: The program implements a timer that the game players must complete their choice within to play the game.
- GUI Display: The GUI displays 4 main configurations of the window to simulate the price is right game. The first part is the base loading screen. The following three configurations of the main window are the games 1-3 that are changed based on what the user has provided.
- HardWare: The user will need 2 SpectreSymbol soft potentiometers. 1 breadboard. One USB chord and 10 wires. 
### System Design:
- The game has three STM32 modules that interface with the PyQt Gui.
- The game transfers the raw potentiometer values for each softpot along with the current timer over serial. These values are sent over serial as a comma seperated list in which these are parsed into a list in Python.
### System Block Diagram: 
![image](https://github.com/adurkarARIN555/MTRX2700-Game-Show/assets/160560741/2a843a68-242b-4861-8263-013f6089d3a2)


### Instructions for use:  
#### Before gameplay:
1. Assemble the board as shown in the picture with the wiper of each soft potentiometer connected to the pin that has been chosen in the IOC.
![image](https://github.com/adurkarARIN555/MTRX2700-Game-Show/assets/160560741/446d4164-70b6-411a-b94e-893f1886ab8d)






#### During Game Play:
1. Plug the STM32 into the computer with the project already loaded. Once the microcontroller is running with the code for the game then enter all the data into the main window and press "Start game"
2. The game needs 4 players in which the first two games are played by all 4 users. The final game is played by the losers from games 1 and 2.
3. Once Start Game is pressed the default start window for the game will display. The reset button can be clicked on the microcontroller to switch to each game configuration.
4. The user will have 15 seconds in total to make a decision on the price of the object including 3 seconds to observe the image and 12 seconds to make a decision.
5. A decision can be made by using either of the sliders and the player that has successfully guessed the price that is closest to the actual price of the image object will win.
6. Once the timer runs out in every game a decision on the price can no longer be made.
7. When the end of the game is reached the loser is tehn sent to the mainwindow and displayed.
### Testing:
### Performance:
- The current slider value represents current resistance from the potentiometer at that time.
- The dial gui widget represents the current time that TIM2 is counting.
### Individual Modules:
- ```Timer```: The timer module sends over a serial a continuous timer signal that is only restarted once the STM reset button is pressed.
- ```HAL PWM```: The HAL_PWM is 
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
-	```HAL PWM```: This module is configured to rotate the servo motors to a certain angle using ```TIM2```. The control register ```CCR1``` controls the release mechanism servo while ```CCR2``` controls the spring loading servo.

![MTRX2700 Flowchart](https://github.com/adurkarARIN555/MTRX2700-Game-Show/assets/160400819/66abc03f-5e2a-4cd2-95ed-197918b31efc)

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
1. Press the Blue User Button on the STM32.
2. Observe the LED movement and try to get maximum LEDs ON. (More LED’s, more strength).
3. The load will be shot with power corresponding to the number of switched-ON LEDs.
4. After the load lands at a certain distance, we the judges measure the distance and the participant having the load shot furthest is promoted to the final level of the game.
5. Wait for the game to reset and play again.

### Testing:
- The function ```run_tests``` initializes serial communication and runs a number of tests checking the working of various functions related to LEDs, servo motors strength, PWM.
- Test Case 1: Verifies that ```countLED``` function correctly counts the number of ON LEDs in the binary representation checking if the value equals 5. If not correctly executed, the test case fails.
- Test Case 2: Verifies that the  ```countLED```  function counts that the number of LEDs ON are 4.
- Test Case 3: Checks that the strength (angle) of shooting the load from the catapult is 2250 when 6 LEDs are ON.
- Test Case 4 and 5: Are responsible to check the LED functions. Firstly, the LEDs are set to all zeros (all OFF), then, there is an increment in the number of LEDs by 1 and the TEST_ASSERT functions tests if the new state is ‘0b01111111’. Test Case 5 also does the same verification but with different number of LEDs.
- In case any test case fails, a message is sent to the Serial port (USART1) and the program “exits”. If all tests pass, “All test cases passed” is output on the Serial port.


### Performance:
- The number of LEDs that are ON correspond to the angle the servo motor will turn.
- Higher angle means that the spring in the catapult is stretched more and creates a strong force for the load to be shot with a greater speed.
- The benchtop power supply is used to power the big servo motor that runs on 6 to 7.4V and is responsible to stretch the springs to the particular angles.
- The small servo motor is run on 5V and is given power from a power supply by connecting it through a breadboard.
- The 3 springs are a perfect fit for the load to be shot to a long distance. We had also tried the system with 4 springs, but the required force was not generated as the spring constant was too small. We also tried with 2 springs, but the servo struggled a little to handle the load.

![Figure_1](https://github.com/adurkarARIN555/MTRX2700-Game-Show/assets/160400819/e9c8b9b3-b888-45ce-a14f-7a35ae12f6c6)


## Mario Kart:
### Requirement Specification: 
- A two-player kart racing game was designed with the desire to replicate the mechanics of Mario Kart Wii.
- Two STM32F3 microcontrollers are to be used, connected to a single computer through two different COM ports.
- Rotation of the microcontroller should turn the steering of the vehicle, and pressing or releasing the user button should modulate the velocity of the kart.
- The first player to complete three laps of the course will survive, with the other player being eliminated.

### System Design:
![GAME3-basic_v2 drawio](https://github.com/adurkarARIN555/MTRX2700-Game-Show/assets/160551764/ca61eca4-69ee-477b-a054-90c496f15959)

A very high-level functional block diagram shows the design of the current system. The gyroscope on the microcontroller measures the change in rotation of the microcontroller. This is used to rotate the steering axis of the kart. The blue USER button on the microcontroller modulates the velocity of the kart, working by accelerating the kart up to a maximal threshold when the button is pressed, and decelerating the kart down to a minimal threshold when the button is released. These inputs are given to the computer from the COM ports where a python script is displaying a GUI. The gyroscope values are sent back to the microcontroller via USART1 velocity and position values are calculated on the microcontroller and then updated on the GUI. Where the position value is calculated to be outside of the bounds of the track, the kart is respawned back to the start of the track. 

A checkpoint system was developed to ensure no player can continuously drive backwards and forwards to cheat the lap count system. Once the checkpoint is passed (located halfway along the track), the lap counter is enabled and will be incremented once the finish line is passed. Where the player has passed the checkpoint, but then crashes their kart (position calculated outside of the track bounds), their checkpoint flag is reset. This ensures no player can pass the checkpoint, then intentionally crash to respawn near the finish line and then have their lap count increased. 

### Detailed Design: 
![GAME3-detailed drawio](https://github.com/adurkarARIN555/MTRX2700-Game-Show/assets/160551764/e3b4c3ad-121e-4958-a579-23dc26791b86)

### Instructions for use:  
1. Connect both STM32F3 microcontrollers to the single computer.
2. Hold the microcontroller level before the race starts (this will ensure the steering is referenced from a comfortable position).
3. Look at the LEDs on the microcontroller, the green LEDs indicates that microcontroller is Luigi and will control the green kart, similarly, is the LEDs are red, that indicated that micrcontroller is Mario and will control the red kart.
4. Hold down the blue USER button to accelerate the kart, and let go to decelerate.
5. Tilt the micrcontroller along the z-axis, the same way you would rotate a car's steering wheel, to rotate the steering angle of the kart.
6. The game will finish once the one of the players completes three laps.

### Testing:
run the tests module
(explain what each of these will do)

### Performance:

