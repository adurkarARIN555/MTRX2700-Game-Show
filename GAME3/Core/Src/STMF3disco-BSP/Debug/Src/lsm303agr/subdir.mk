################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Src/lsm303agr/lsm303agr.c 

OBJS += \
./Src/lsm303agr/lsm303agr.o 

C_DEPS += \
./Src/lsm303agr/lsm303agr.d 


# Each subdirectory must supply rules for building sources it contributes
Src/lsm303agr/%.o Src/lsm303agr/%.su Src/lsm303agr/%.cyclo: ../Src/lsm303agr/%.c Src/lsm303agr/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -DDEBUG -DUSE_HAL_DRIVER -DSTM32F303xC -c -I../Drivers/CMSIS/Device/ST/STM32F3xx/Include -I../Drivers/CMSIS/Include -I../Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc -I../Drivers/STM32F3xx_HAL_Driver/Inc/Legacy -I../Src -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Src-2f-lsm303agr

clean-Src-2f-lsm303agr:
	-$(RM) ./Src/lsm303agr/lsm303agr.cyclo ./Src/lsm303agr/lsm303agr.d ./Src/lsm303agr/lsm303agr.o ./Src/lsm303agr/lsm303agr.su

.PHONY: clean-Src-2f-lsm303agr

