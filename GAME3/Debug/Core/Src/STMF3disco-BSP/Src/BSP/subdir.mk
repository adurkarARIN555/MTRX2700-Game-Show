################################################################################
# Automatically-generated file. Do not edit!
# Toolchain: GNU Tools for STM32 (11.3.rel1)
################################################################################

# Add inputs and outputs from these tool invocations to the build variables 
C_SRCS += \
../Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.c \
../Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.c \
../Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.c \
../Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.c \
../Core/Src/STMF3disco-BSP/Src/BSP/syscalls.c \
../Core/Src/STMF3disco-BSP/Src/BSP/sysmem.c 

OBJS += \
./Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.o \
./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.o \
./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.o \
./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.o \
./Core/Src/STMF3disco-BSP/Src/BSP/syscalls.o \
./Core/Src/STMF3disco-BSP/Src/BSP/sysmem.o 

C_DEPS += \
./Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.d \
./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.d \
./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.d \
./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.d \
./Core/Src/STMF3disco-BSP/Src/BSP/syscalls.d \
./Core/Src/STMF3disco-BSP/Src/BSP/sysmem.d 


# Each subdirectory must supply rules for building sources it contributes
Core/Src/STMF3disco-BSP/Src/BSP/%.o Core/Src/STMF3disco-BSP/Src/BSP/%.su Core/Src/STMF3disco-BSP/Src/BSP/%.cyclo: ../Core/Src/STMF3disco-BSP/Src/BSP/%.c Core/Src/STMF3disco-BSP/Src/BSP/subdir.mk
	arm-none-eabi-gcc "$<" -mcpu=cortex-m4 -std=gnu11 -g3 -c -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Core/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/STM32F3xx_HAL_Driver/Inc/Legacy" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Device/ST/STM32F3xx/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/W10-embedded-sensors/Drivers/CMSIS/Include" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Inc" -I"C:/Users/61411/OneDrive/Desktop/MTRX2700-2024/STMF3disco-BSP/Src" -O0 -ffunction-sections -fdata-sections -Wall -fstack-usage -fcyclomatic-complexity -MMD -MP -MF"$(@:%.o=%.d)" -MT"$@" --specs=nano.specs -mfpu=fpv4-sp-d16 -mfloat-abi=hard -mthumb -o "$@"

clean: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src-2f-BSP

clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src-2f-BSP:
	-$(RM) ./Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.cyclo ./Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.d ./Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.o ./Core/Src/STMF3disco-BSP/Src/BSP/F3-disco-BSP.su ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.cyclo ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.d ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.o ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery.su ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.cyclo ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.d ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.o ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_accelerometer.su ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.cyclo ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.d ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.o ./Core/Src/STMF3disco-BSP/Src/BSP/stm32f3_discovery_gyroscope.su ./Core/Src/STMF3disco-BSP/Src/BSP/syscalls.cyclo ./Core/Src/STMF3disco-BSP/Src/BSP/syscalls.d ./Core/Src/STMF3disco-BSP/Src/BSP/syscalls.o ./Core/Src/STMF3disco-BSP/Src/BSP/syscalls.su ./Core/Src/STMF3disco-BSP/Src/BSP/sysmem.cyclo ./Core/Src/STMF3disco-BSP/Src/BSP/sysmem.d ./Core/Src/STMF3disco-BSP/Src/BSP/sysmem.o ./Core/Src/STMF3disco-BSP/Src/BSP/sysmem.su

.PHONY: clean-Core-2f-Src-2f-STMF3disco-2d-BSP-2f-Src-2f-BSP

