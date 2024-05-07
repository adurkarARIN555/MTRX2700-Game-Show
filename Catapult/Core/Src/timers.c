#include <timers.h>
#include <stdio.h>
#include "stm32f303xc.h"

#define PRESCALER 0x176F
#define MILLISECOND_SCALAR 8

// pointer to callback function for continuous timer
void (*continuous_callback_function)();
// pointer to callback function for oneshot timer
void (*oneshot_callback_function)();

void enable_interrupt(IRQn_Type NVIC_module, uint32_t priority) {
	// Disable the interrupts while messing around with the settings
	//  otherwise can lead to strange behaviour
	__disable_irq();

	// Tell the NVIC module that TIM2 interrupts should be handled
	NVIC_SetPriority(NVIC_module, priority);  // Set Priority
	NVIC_EnableIRQ(NVIC_module);

	// Re-enable all interrupts (now that we are finished)
	__enable_irq();
}

void TIM2_IRQHandler(){
	// run the continuous timer interrupt handler
	if (TIM2->SR & TIM_SR_UIF) {
		TIM2->SR &= ~TIM_SR_UIF; // clear continuous timer interrupt
		continuous_callback_function();
	}

}

void timer_initialise(uint16_t interval, void (*callback_function)()) {

	// reset CR1
	TIM2->CR1 = 0x00;

	// enable counter
	TIM2->CR1 |= TIM_CR1_CEN;

	// set the prescaler to 5999, slower than the default clock 6000 times, Clock speed 48MHz
	TIM2->PSC = PRESCALER; // 125 microseconds = 0.125 milliseconds per count

	// set the auto reload according to the prescaler
	TIM2->ARR = MILLISECOND_SCALAR; // 8 - 1 millisecond
	TIM2->ARR = TIM2->ARR * interval; // interval in millisecond
	TIM2->CR1 |= TIM_CR1_ARPE; // enable auto reload buffering

	// set to only counter overflow raises interrupt flag
	TIM2->CR1 |= TIM_CR1_URS;

	// re-initialise the counter and generates an update of the registers
	TIM2->EGR |= TIM_EGR_UG;

	// enable the update interrupt
	TIM2->DIER |= TIM_DIER_UIE;

	// clear the interrupt
	TIM2->SR &= ~TIM_SR_UIF;

	continuous_callback_function = callback_function;

	enable_interrupt(TIM2_IRQn, 3);

}

void TIM3_IRQHandler(){
// run the oneshot timer interrupt handler
	if (TIM3->SR & TIM_SR_UIF) {
		// clear oneshot timer interrupt
		TIM3->SR &= ~TIM_SR_UIF;

		if (oneshot_callback_function != NULL)
		{
			oneshot_callback_function();
		}

		// enable counter
		TIM3->CR1 &= TIM_CR1_CEN;

	}

}

void trigger_oneshot(uint16_t delay, void (*callback_function)()) {

	// reset CR1
	TIM3->CR1 = 0x00;

	// enable counter
	TIM3->CR1 |= TIM_CR1_CEN;

	// set the prescaler to 5999, slower than the default clock 6000 times, clock speed 48MHz
	TIM3->PSC = PRESCALER; // 125 microseconds = 0.125 milliseconds per count

	// set the auto reload according to the prescaler
	TIM3->ARR = 0x08; // 8 - 1 millisecond
	TIM3->ARR = TIM3->ARR * delay; // delay in millisecond
	TIM3->CR1 |= TIM_CR1_ARPE; // enable auto reload buffering

	// set to only counter overflow raises interrupt flag
	TIM3->CR1 |= TIM_CR1_URS;

	// re-initialise the counter and generates an update of the registers
	TIM3->EGR |= TIM_EGR_UG;

	// enable the update interrupt
	TIM3->DIER |= TIM_DIER_UIE;

	// clear the interrupt
	TIM3->SR &= ~TIM_SR_UIF;

	oneshot_callback_function = callback_function;

	enable_interrupt(TIM3_IRQn,2);

}

uint32_t get_time(void)
{
	//return the time in ms
	return TIM2->ARR/MILLISECOND_SCALAR;
}

void set_time(uint32_t interval)
{
	//Stops TIM2
	TIM2->CR1 &= ~TIM_CR1_CEN;

	// Update the auto-reload value
	TIM2->ARR = interval*MILLISECOND_SCALAR;

	// Clear the update flag
	TIM2->SR &= ~TIM_SR_UIF;

	// Start TIM2
	TIM2->CR1 |= TIM_CR1_CEN;
}
