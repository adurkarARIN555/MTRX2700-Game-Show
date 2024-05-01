################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/STMF3disco-BSP/Src/F3-components.c \
../Core/Src/STMF3disco-BSP/Src/syscalls.c \
../Core/Src/STMF3disco-BSP/Src/sysmem.c 

OBJS += \
./Core/Src/STMF3disco-BSP/Src/F3-components.o \
./Core/Src/STMF3disco-BSP/Src/syscalls.o \
./Core/Src/STMF3disco-BSP/Src/sysmem.o 

C_DEPS += \
./Core/Src/STMF3disco-BSP/Src/F3-components.d \
./Core/Src/STMF3disco-BSP/Src/syscalls.d \
./Core/Src/STMF3disco-BSP/Src/sysmem.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/STMF3disco-BSP/Src/%.o Core/Src/STMF3disco-BSP/Src/%.su Core/Src/STMF3disco-BSP/Src/%.cyclo: ../Core/Src/STMF3disco-BSP/Src/%.c Core/Src/STMF3disco-BSP/Src/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -c -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Core/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Device/ST/STM32F3xx/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Src" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src

clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src:
	-$(RM) ./Core/Src/STMF3disco-BSP/Src/F3-components.cyclo ./Core/Src/STMF3disco-BSP/Src/F3-components.d ./Core/Src/STMF3disco-BSP/Src/F3-components.o ./Core/Src/STMF3disco-BSP/Src/F3-components.su ./Core/Src/STMF3disco-BSP/Src/syscalls.cyclo ./Core/Src/STMF3disco-BSP/Src/syscalls.d ./Core/Src/STMF3disco-BSP/Src/syscalls.o ./Core/Src/STMF3disco-BSP/Src/syscalls.su ./Core/Src/STMF3disco-BSP/Src/sysmem.cyclo ./Core/Src/STMF3disco-BSP/Src/sysmem.d ./Core/Src/STMF3disco-BSP/Src/sysmem.o ./Core/Src/STMF3disco-BSP/Src/sysmem.su

.PHONY: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src

