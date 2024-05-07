#include <stdio.h>
#include <stdint.h>
#include "digital_io.h"
#include "timers.h"

#include "stm32f303xc.h"

#define PATTERN_1 0b01010101
#define PATTERN_2 0b10101010
#define ALL_ON 0b11111111
#define ERROR_LED 0b00000010

#pragma GCC diagnostic ignored "-Wpointer-sign"

void (*on_button_press)() = 0x00;
uint32_t counter_flag = 0;

// enable the clocks for desired peripherals (GPIOA, C and E)
void enable_clocks()
{

	RCC->AHBENR |= RCC_AHBENR_GPIOAEN | RCC_AHBENR_GPIOCEN | RCC_AHBENR_GPIOEEN;

	RCC->APB1ENR |=  RCC_APB1ENR_TIM2EN;
	RCC->APB1ENR |=  RCC_APB1ENR_TIM3EN;

}

// initialise the discovery board I/O
void initialise_board()
{

	// get a pointer to the second half word of the MODER register (for outputs pe8-15)
	uint16_t *led_output_registers = ((uint16_t *)&(GPIOE->MODER)) + 1;
	*led_output_registers = 0x5555;

}

void EXTI0_IRQHandler(void)
{
	// run the button press handler (make sure it is not null first !)
	if (on_button_press != 0x00) {
		on_button_press();
	}

	// reset the interrupt (so it doesn't keep firing until the next trigger)
	EXTI->PR |= EXTI_PR_PR0;
}

void enable_button_interrupt(void (*func_ptr)(void))
{
	// Disable the interrupts while messing around with the settings
	//  otherwise can lead to strange behaviour
	__disable_irq();

	// Enable the system configuration controller (SYSCFG in RCC)
	RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;

	// External Interrupts details on large manual page 294)
	// PA0 is on interrupt EXTI0 large manual - page 250
	// EXTI0 in  SYSCFG_EXTICR1 needs to be 0x00 (SYSCFG_EXTICR1_EXTI0_PA)
	SYSCFG->EXTICR[0] = SYSCFG_EXTICR1_EXTI0_PA;

	//  Select EXTI0 interrupt on rising edge
	EXTI->RTSR |= EXTI_RTSR_TR0; // rising edge of EXTI line 0 (includes PA0)

	// set the interrupt from EXTI line 0 as 'not masked' - as in, enable it.
	EXTI->IMR |= EXTI_IMR_MR0;

	// Tell the NVIC module that EXTI0 interrupts should be handled
	NVIC_SetPriority(EXTI0_IRQn, 1);  // Set Priority
	NVIC_EnableIRQ(EXTI0_IRQn);

	on_button_press = func_ptr;

	// Re-enable all interrupts (now that we are finished)
	__enable_irq();
}

//set function takes binary number and turns on LEDs
void set_LED(uint8_t binaryNumber)
{
	if (binaryNumber <= 255 && binaryNumber >= 0)
	{
		uint8_t *led_register = ((uint8_t*)&(GPIOE->ODR)) + 1;
		*led_register = binaryNumber;
	}
	else
	{
		uint8_t *led_register = ((uint8_t*)&(GPIOE->ODR)) + 1;
		*led_register = ERROR_LED;
	}

}

//get function returns binary/decimal number from current LED state
uint8_t get_LED()
{
	uint8_t *led_register = ((uint8_t*)&(GPIOE->ODR)) + 1;
	uint8_t binaryNumber = *led_register;
	return binaryNumber;
}

void led_increase()
{
	if (counter_flag == 0)
	{
		set_LED(0b00000001 | (get_LED() << 1));
		if (get_LED() == 0b11111111)
		{
			counter_flag = 1;
		}
	}
	else if (counter_flag == 1)
	{
		set_LED(get_LED() >> 1);
		if (get_LED() == 0b00000000)
		{
			counter_flag = 0;
		}
	}

}


