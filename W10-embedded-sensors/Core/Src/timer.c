#include <stdint.h>
#include "stm32f303xc.h"
#include "timer.h"
#include "serial.h"
#include <stdio.h>
#include "string.h"
void (*finished_interval)(void) = 0x00;

uint32_t newPeriod = 5000;
uint8_t leds = 0;
uint8_t continous_mode = 0; // j
uint8_t one_shot_mode = 0;// j

void one_shot_func(void) {
	if ((TIM2->CR1 & TIM_CR1_CEN) == 0) {		// check timer currently running
        TIM2->CNT = 0x00; 						// Reset the counter
	    TIM2->ARR = newPeriod - 1; 				// Set the auto-reload value
        TIM2->CR1 |= TIM_CR1_CEN; 				// Start the timer
        leds = 1; 								// Set LEDs to ON state
	}
}

// The purpose of this function is to reset the current mode the timer is working
// Doing this ensures that only one mode is currently running at a time
void reset_modes(){
	continous_mode = 0;							// Resets continous mode
	one_shot_mode = 0;							// Resets one shot mode
}

// This function intialises the callback function and sets the mode to oneshot mode
void one_shot(uint32_t period, void(*display_func)(void)){
	reset_modes();// j
	one_shot_mode = 1; // j

	newPeriod = period;
	finished_interval = display_func;

}

// This function intialises the callback function and sets the mode to continous mode
void interval_mode(uint32_t period, void(*display_func)(void)){// j
	reset_modes();
	continous_mode = 1;
	newPeriod = period;// j
	set_period(newPeriod);//j
	TIM2->CR1 |= TIM_CR1_CEN; 					// enable timer2
	finished_interval = display_func;// j
}// j

// This function changes the current period
void set_period(uint32_t period){// j
	TIM2->CNT = 0x00;// j
	TIM2->ARR = newPeriod - 1;// j

}// j


void TIM2_IRQHandler(void) {
	if ((TIM2->SR & TIM_SR_UIF) != 0) {			// check update interrupt flag timer2
        TIM2->SR &= ~TIM_SR_UIF; 				// Clear the update interrupt flag
        										// Set LEDs to OFF state after timer expires
        //display(); 								// Update the LEDs to OFF state
        if (finished_interval != 0x00){
        	finished_interval();
        }

	}
}

void enable_interrupt_timer2(void) {
    __disable_irq();
    TIM2->DIER |= TIM_DIER_UIE; 				// Enable update interrupt for timer 2
    NVIC_SetPriority(TIM2_IRQn, 0); 			// Set Priority
    NVIC_EnableIRQ(TIM2_IRQn); 					// Enable interrupts for timer 2
    __enable_irq();
}

void trigger_prescaler(uint32_t periodInSeconds) {
    TIM2->CR1 = 0;
    TIM2->PSC = 7999;

    TIM2->ARR = periodInSeconds - 1;
    TIM2->EGR = TIM_EGR_UG;
}

void display(void) {
    uint8_t *led_output_register = ((uint8_t*)&(GPIOE->ODR)) + 1;
    *led_output_register = leds ? 0xFF : 0x00; 		// Update LEDs based on 'leds' state
}


