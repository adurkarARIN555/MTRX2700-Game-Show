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

void led_increase();

#endif
