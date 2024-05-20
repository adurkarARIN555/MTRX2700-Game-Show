#ifndef TIMERS_HEADER
#define TIMERS_HEADER

#include <stdint.h>

#include "stm32f303xc.h"

// enable timer interrupts
// input: interrupt to enable and priority
void enable_interrupt(IRQn_Type NVIC_module, uint32_t priority);

// timer_iniitialise: run the callback function continuously at the input interval
// Input: interval in millisecond, pointer to the callback function
void timer_initialise(uint16_t interval, void (*callback_function)());

//triggers oneshot timer with delay in ms and callback function
void trigger_oneshot(uint16_t delay, void (*callback_function)());

//returns the time interval the timer is running at currently in ms
uint32_t get_time(void);

//resets the timer to a new period specified as interval
void set_time(uint32_t interval);


#endif
