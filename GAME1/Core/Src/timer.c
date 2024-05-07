#include <stdint.h>
#include "stm32f303xc.h"
#include "timer.h"
#include "serial.h"

void (*finished_interval)() = 0x00;
uint32_t newPeriod = 5000;
uint8_t continous_mode = 0;
uint8_t one_shot_mode = 0;

uint16_t elapsed_time = 0;

// Initialise timer module, sets the desired callback
void timer_initialise(uint16_t timer_period, void (*callback)()){
	trigger_prescaler(timer_period);			// Trigger prescaler with intial period
	enable_interrupt_timer2();
	finished_interval = callback;				// Set the desired call back
												// for the timer module
}

void one_shot_func(void){
	if ((TIM2->CR1 & TIM_CR1_CEN) == 0){		// Check timer intialised
		TIM2->CNT = 0x00;						// Reset the count
		TIM2->ARR = newPeriod-1;
		TIM2->CR1 |= TIM_CR1_CEN;
	}
}

// The purpose of this function is to reset the timer mode and elapsed time
// that is going to be displayed
void reset_modes(){
	elapsed_time = 0;
	continous_mode = 0;
	one_shot_mode = 0;
}

// Intialise oneshot, set the period of oneshot, and change the mode
void one_shot(uint32_t period){
	TIM2->CR1 &= ~TIM_CR1_CEN;					// Ensures timer is not already running
	reset_modes();
	one_shot_mode = 1;							// Change the current mode of the timer module

	newPeriod = period;
}

// Initialise interval mode for a continous timer action
void interval_mode(uint32_t period){
	reset_modes();
	continous_mode = 1;
	newPeriod = period;
	set_period(newPeriod);
	TIM2->CR1 |= TIM_CR1_CEN;
}

// The purpose of this function is to change the period of the timer
void set_period(uint32_t period){
	TIM2->CNT = 0x00;
	TIM2->ARR = period - 1;
	newPeriod = period;
}

// The purpose of this function is to get the current period of the timer
uint32_t get_period(){
	return newPeriod;
}

// The purpose of this function is to deal with interrupts for the timer based upon
// the value of current timer count in comparison to the timer period set in hardware
void TIM2_IRQHandler(void){
	if ((TIM2->SR & TIM_SR_UIF) != 0){
		TIM2->SR &= ~TIM_SR_UIF;
		if (one_shot_mode){
			TIM2->CR1 &= ~TIM_CR1_CEN;			// Timer is disabled afterward for a oneshot
			if (finished_interval != 0x00){
				finished_interval();
			}
		}
		if (continous_mode){
			if (finished_interval != 0x00){
				finished_interval();
			}
		}


	}
}

// Enables the interrupts for timer2 to ensure that they can be caught
void enable_interrupt_timer2(void){
	__disable_irq();
	TIM2->DIER |= TIM_DIER_UIE;
	NVIC_SetPriority(TIM2_IRQn, 1);
	NVIC_EnableIRQ(TIM2_IRQn);
	__enable_irq;
}

// Trigger the prescaler so that the period can be passed in milliseconds
void trigger_prescaler(uint32_t period_in_milliseconds){
	TIM2->CR1 = 0;
	TIM2->PSC = 7999;
	TIM2->ARR = period_in_milliseconds - 1;
	TIM2->EGR = TIM_EGR_UG;
}
