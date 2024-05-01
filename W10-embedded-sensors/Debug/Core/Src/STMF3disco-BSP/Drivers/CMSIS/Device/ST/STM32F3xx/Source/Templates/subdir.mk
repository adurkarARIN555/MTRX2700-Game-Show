################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.c 

OBJS += \
./Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.o 

C_DEPS += \
./Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/%.o Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/%.su Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/%.cyclo: ../Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/%.c Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -c -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Core/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Device/ST/STM32F3xx/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Src" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Drivers-2f-CMSIS-2f-Device-2f-ST-2f-STM32F3xx-2f-Source-2f-Templates

clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Drivers-2f-CMSIS-2f-Device-2f-ST-2f-STM32F3xx-2f-Source-2f-Templates:
	-$(RM) ./Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.cyclo ./Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.d ./Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.o ./Core/Src/STMF3disco-BSP/Drivers/CMSIS/Device/ST/STM32F3xx/Source/Templates/system_stm32f3xx.su

.PHONY: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Drivers-2f-CMSIS-2f-Device-2f-ST-2f-STM32F3xx-2f-Source-2f-Templates

