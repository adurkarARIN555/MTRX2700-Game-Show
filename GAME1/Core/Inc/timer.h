#ifndef TIMER_H_
#define TIMER_H_

void one_shot_func(void);
void TIM2_IRQHandler(void);
void enable_interrupt_timer2(void);
void trigger_prescaler(uint32_t periodInSeconds);
void display(void);
void one_shot(uint32_t period);//, void(*display_func)(void));//j
void interval_mode(uint32_t period);//j
void reset_modes();
void set_period(uint32_t period);
void enable_clocks();
void timer_initialise(uint16_t timer_period, void (*callback)());
#endif /* TIMER_H_ */
