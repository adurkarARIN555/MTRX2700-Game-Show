################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.c 

OBJS += \
./Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.o 

C_DEPS += \
./Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/STMF3disco-BSP/Src/lsm303agr/%.o Core/Src/STMF3disco-BSP/Src/lsm303agr/%.su Core/Src/STMF3disco-BSP/Src/lsm303agr/%.cyclo: ../Core/Src/STMF3disco-BSP/Src/lsm303agr/%.c Core/Src/STMF3disco-BSP/Src/lsm303agr/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -c -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Core/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Device/ST/STM32F3xx/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Src" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src-2f-lsm303agr

clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src-2f-lsm303agr:
	-$(RM) ./Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.cyclo ./Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.d ./Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.o ./Core/Src/STMF3disco-BSP/Src/lsm303agr/lsm303agr.su

.PHONY: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src-2f-lsm303agr

