#include <stdio.h>
#include "serial.h"

#include "stm32f303xc.h"

// We store the pointers to the GPIO and USART that are used
struct _SerialPort
{
	USART_TypeDef *UART;
	GPIO_TypeDef *GPIO;
	volatile uint32_t MaskAPB2ENR;	// mask to enable RCC APB2 bus registers
	volatile uint32_t MaskAPB1ENR;	// mask to enable RCC APB1 bus registers
	volatile uint32_t MaskAHBENR;	// mask to enable RCC AHB bus registers
	volatile uint32_t SerialPinModeValue;
	volatile uint32_t SerialPinSpeedValue;
	volatile uint32_t SerialPinAlternatePinValueLow;
	volatile uint32_t SerialPinAlternatePinValueHigh;
	volatile IRQn_Type USART_IRQn;
	void (*completion_function)(uint32_t, uint8_t*);
};


// instantiate the serial port parameters
SerialPort USART1_PORT = {USART1,
		GPIOC,
		RCC_APB2ENR_USART1EN, // bit to enable for APB2 bus
		0x00,	// bit to enable for APB1 bus
		RCC_AHBENR_GPIOCEN, // bit to enable for AHB bus
		0xA00,
		0xF00,
		0x770000,  // for USART1 PC4 and 5, this is in the AFR low register
		0x00, // no change to the high alternate function register
		USART1_IRQn, //interrupts enable
		0x00 // default function pointer is NULL
		};


// InitialiseSerial - Initialise the serial port
// Input: baudRate is from an enumerated set
void SerialInitialise(uint32_t baudRate, SerialPort *serial_port, void (*completion_function)(uint32_t, uint8_t*))
{

	serial_port->completion_function = completion_function;

	// enable clock power, system configuration clock and GPIOC
	// common to all UARTs
	RCC->APB1ENR |= RCC_APB1ENR_PWREN;
	RCC->APB2ENR |= RCC_APB2ENR_SYSCFGEN;

	// enable the GPIO which is on the AHB bus
	RCC->AHBENR |= serial_port->MaskAHBENR;

	// set pin mode to alternate function for the specific GPIO pins
	serial_port->GPIO->MODER = serial_port->SerialPinModeValue;

	// enable high speed clock for specific GPIO pins
	serial_port->GPIO->OSPEEDR = serial_port->SerialPinSpeedValue;

	// set alternate function to enable USART to external pins
	serial_port->GPIO->AFR[0] |= serial_port->SerialPinAlternatePinValueLow;
	serial_port->GPIO->AFR[1] |= serial_port->SerialPinAlternatePinValueHigh;

	// enable the device based on the bits defined in the serial port definition
	RCC->APB1ENR |= serial_port->MaskAPB1ENR;
	RCC->APB2ENR |= serial_port->MaskAPB2ENR;

	// Get a pointer to the 16 bits of the BRR register that we want to change
	uint16_t *baud_rate_config = (uint16_t*)&serial_port->UART->BRR;

	// Baud rate calculation from datasheet
	switch(baudRate)
	{

		case BAUD_9600:
			*baud_rate_config = 0x341;  // 9600 at 8MHz
			break;
		case BAUD_19200:
			*baud_rate_config = 0x1A1;  // 19200 at 8MHz
			break;
		case BAUD_38400:
			*baud_rate_config = 0xD0;  // 38400 at 8MHz
			break;
		case BAUD_57600:
			*baud_rate_config = 0x8B;  // 57600 at 8MHz
			break;
		case BAUD_115200:
			*baud_rate_config = 0x46;  // 115200 at 8MHz
			break;
	}


	// enable serial port for tx and rx
	serial_port->UART->CR1 |= USART_CR1_TE | USART_CR1_RE | USART_CR1_UE| USART_CR1_RXNEIE;
}

void EnableUartInterrupts(SerialPort *serial_port)
{
	NVIC_EnableIRQ(serial_port->USART_IRQn);
}


void SerialOutputChar(uint8_t data, SerialPort *serial_port)
{

	while((serial_port->UART->ISR & USART_ISR_TXE) == 0)	{}
	serial_port->UART->TDR = data;
}

void SerialOutputString(uint8_t *pt, SerialPort *serial_port)
{
	//each character is sent and count increased
	uint32_t counter = 0;
	while(*pt)
	{
		SerialOutputChar(*pt, serial_port);
		counter++;
		pt++;
	}
}

uint8_t SerialInputChar(SerialPort *serial_port)
{
	while (serial_port->UART->ISR & (USART_ISR_ORE | USART_ISR_FE))
	{
		// If ORE or FE is set, read USART_RDR to clear the flags
		volatile uint32_t temp = USART1->RDR;
		(void)temp; // To avoid unused variable warning
	}

	while((serial_port->UART->ISR & USART_ISR_RXNE) == 0)	{}

	//read in a character at a time and return it
	uint8_t character = serial_port->UART->RDR;
	return character;
}

uint8_t* SerialInputString(uint8_t* buffer,uint32_t buffer_size, SerialPort *serial_port, uint8_t termination_char)
{
	//characters are only read until the buffer is full or a termination char is sent
	uint32_t counter = 0;
	for (uint32_t i = 0; i < buffer_size/sizeof(uint8_t);i++)
	{
		uint8_t character = SerialInputChar(serial_port);
		buffer[i] = character;
		counter++;
		if (character == termination_char)
		{
			break;
		}
	}
	//callback is called if not equal to NULL
	if (serial_port->completion_function != NULL)
	{
		serial_port->completion_function(counter,buffer);
	}
	return buffer;
}
