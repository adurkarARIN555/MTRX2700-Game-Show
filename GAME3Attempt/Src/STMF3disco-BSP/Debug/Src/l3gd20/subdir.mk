################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/l3gd20/l3gd20.c 

OBJS += \
./Src/l3gd20/l3gd20.o 

C_DEPS += \
./Src/l3gd20/l3gd20.d 


# Each subdirectory must supply rules for building sources it contributes
Src/l3gd20/%.o Src/l3gd20/%.su Src/l3gd20/%.cyclo: ../Src/l3gd20/%.c Src/l3gd20/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F303xC -c -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I../Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Src -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src-2f-l3gd20

clean-Src-2f-l3gd20:
	-$(RM) ./Src/l3gd20/l3gd20.cyclo ./Src/l3gd20/l3gd20.d ./Src/l3gd20/l3gd20.o ./Src/l3gd20/l3gd20.su

.PHONY: clean-Src-2f-l3gd20

