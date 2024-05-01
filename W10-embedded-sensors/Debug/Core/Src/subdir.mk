################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/main.c \
../Core/Src/serial.c \
../Core/Src/serialise.c \
../Core/Src/stm32f3xx_hal_msp.c \
../Core/Src/stm32f3xx_it.c \
../Core/Src/syscalls.c \
../Core/Src/sysmem.c \
../Core/Src/system_stm32f3xx.c 

OBJS += \
./Core/Src/main.o \
./Core/Src/serial.o \
./Core/Src/serialise.o \
./Core/Src/stm32f3xx_hal_msp.o \
./Core/Src/stm32f3xx_it.o \
./Core/Src/syscalls.o \
./Core/Src/sysmem.o \
./Core/Src/system_stm32f3xx.o 

C_DEPS += \
./Core/Src/main.d \
./Core/Src/serial.d \
./Core/Src/serialise.d \
./Core/Src/stm32f3xx_hal_msp.d \
./Core/Src/stm32f3xx_it.d \
./Core/Src/syscalls.d \
./Core/Src/sysmem.d \
./Core/Src/system_stm32f3xx.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/%.o Core/Src/%.su Core/Src/%.cyclo: ../Core/Src/%.c Core/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -c -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Core/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Device/ST/STM32F3xx/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Src" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src

clean-Core-2f-Src:
	-$(RM) ./Core/Src/main.cyclo ./Core/Src/main.d ./Core/Src/main.o ./Core/Src/main.su ./Core/Src/serial.cyclo ./Core/Src/serial.d ./Core/Src/serial.o ./Core/Src/serial.su ./Core/Src/serialise.cyclo ./Core/Src/serialise.d ./Core/Src/serialise.o ./Core/Src/serialise.su ./Core/Src/stm32f3xx_hal_msp.cyclo ./Core/Src/stm32f3xx_hal_msp.d ./Core/Src/stm32f3xx_hal_msp.o ./Core/Src/stm32f3xx_hal_msp.su ./Core/Src/stm32f3xx_it.cyclo ./Core/Src/stm32f3xx_it.d ./Core/Src/stm32f3xx_it.o ./Core/Src/stm32f3xx_it.su ./Core/Src/syscalls.cyclo ./Core/Src/syscalls.d ./Core/Src/syscalls.o ./Core/Src/syscalls.su ./Core/Src/sysmem.cyclo ./Core/Src/sysmem.d ./Core/Src/sysmem.o ./Core/Src/sysmem.su ./Core/Src/system_stm32f3xx.cyclo ./Core/Src/system_stm32f3xx.d ./Core/Src/system_stm32f3xx.o ./Core/Src/system_stm32f3xx.su

.PHONY: clean-Core-2f-Src

