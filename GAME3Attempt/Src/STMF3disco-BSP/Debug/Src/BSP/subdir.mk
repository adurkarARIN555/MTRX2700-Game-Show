################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/BSP/F3-disco-BSP.c \
../Src/BSP/stm32f3_discovery.c \
../Src/BSP/stm32f3_discovery_accelerometer.c \
../Src/BSP/stm32f3_discovery_gyroscope.c \
../Src/BSP/syscalls.c \
../Src/BSP/sysmem.c 

OBJS += \
./Src/BSP/F3-disco-BSP.o \
./Src/BSP/stm32f3_discovery.o \
./Src/BSP/stm32f3_discovery_accelerometer.o \
./Src/BSP/stm32f3_discovery_gyroscope.o \
./Src/BSP/syscalls.o \
./Src/BSP/sysmem.o 

C_DEPS += \
./Src/BSP/F3-disco-BSP.d \
./Src/BSP/stm32f3_discovery.d \
./Src/BSP/stm32f3_discovery_accelerometer.d \
./Src/BSP/stm32f3_discovery_gyroscope.d \
./Src/BSP/syscalls.d \
./Src/BSP/sysmem.d 


# Each subdirectory must supply rules for building sources it contributes
Src/BSP/%.o Src/BSP/%.su Src/BSP/%.cyclo: ../Src/BSP/%.c Src/BSP/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F303xC -c -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I../Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Src -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src-2f-BSP

clean-Src-2f-BSP:
	-$(RM) ./Src/BSP/F3-disco-BSP.cyclo ./Src/BSP/F3-disco-BSP.d ./Src/BSP/F3-disco-BSP.o ./Src/BSP/F3-disco-BSP.su ./Src/BSP/stm32f3_discovery.cyclo ./Src/BSP/stm32f3_discovery.d ./Src/BSP/stm32f3_discovery.o ./Src/BSP/stm32f3_discovery.su ./Src/BSP/stm32f3_discovery_accelerometer.cyclo ./Src/BSP/stm32f3_discovery_accelerometer.d ./Src/BSP/stm32f3_discovery_accelerometer.o ./Src/BSP/stm32f3_discovery_accelerometer.su ./Src/BSP/stm32f3_discovery_gyroscope.cyclo ./Src/BSP/stm32f3_discovery_gyroscope.d ./Src/BSP/stm32f3_discovery_gyroscope.o ./Src/BSP/stm32f3_discovery_gyroscope.su ./Src/BSP/syscalls.cyclo ./Src/BSP/syscalls.d ./Src/BSP/syscalls.o ./Src/BSP/syscalls.su ./Src/BSP/sysmem.cyclo ./Src/BSP/sysmem.d ./Src/BSP/sysmem.o ./Src/BSP/sysmem.su

.PHONY: clean-Src-2f-BSP

