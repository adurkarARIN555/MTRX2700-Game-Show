################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/i3g4250d/i3g4250d.c 

OBJS += \
./Src/i3g4250d/i3g4250d.o 

C_DEPS += \
./Src/i3g4250d/i3g4250d.d 


# Each subdirectory must supply rules for building sources it contributes
Src/i3g4250d/%.o Src/i3g4250d/%.su Src/i3g4250d/%.cyclo: ../Src/i3g4250d/%.c Src/i3g4250d/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F303xC -c -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I../Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Src -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src-2f-i3g4250d

clean-Src-2f-i3g4250d:
	-$(RM) ./Src/i3g4250d/i3g4250d.cyclo ./Src/i3g4250d/i3g4250d.d ./Src/i3g4250d/i3g4250d.o ./Src/i3g4250d/i3g4250d.su

.PHONY: clean-Src-2f-i3g4250d

