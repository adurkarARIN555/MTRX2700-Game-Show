#ifndef DIGITAL_IO_HEADER
#define DIGITAL_IO_HEADER


#include <stdint.h>

void initialise_board();
void enable_clocks();

void enable_button_interrupt(void (*func_ptr)(void));

//set the LEDs to a specific binary pattern
void set_LED(uint8_t binaryNumber);

//get the current LED pattern
uint8_t get_LED();

//increases the number of LEDs on at any given time
void led_increase();

//count the number of LEDs on given the current state
uint32_t countLED(uint8_t N);

#endif
