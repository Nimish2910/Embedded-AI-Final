#include "main.h"
#include "adc.h"
#include "usart.h"
#include "gpio.h"
#include <string.h>
#include <stdio.h>
#include <stdlib.h>


void SystemClock_Config(void);

#define FILTER_SIZE 8

float temp_buffer[FILTER_SIZE];
int temp_index = 0;


int main(void)
{
    HAL_Init();
    SystemClock_Config();

    MX_GPIO_Init();
    MX_USART1_UART_Init();    // UART to Raspberry Pi
    MX_ADC1_Init();           // ADC init

    char msg[50];
    int len;

    while (1)
    {
        // ---- ADC stabilization sequence ----
        HAL_ADC_Start(&hadc1);
        HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
        HAL_ADC_GetValue(&hadc1);    // Throw away first bad sample

        HAL_ADC_Start(&hadc1);
        HAL_ADC_PollForConversion(&hadc1, HAL_MAX_DELAY);
        uint16_t adc_raw = HAL_ADC_GetValue(&hadc1);

        // ---- Convert ADC to voltage ----
        float Vsense = (adc_raw * 3.3f) / 4095.0f;

        // ---- Convert voltage to temperature ----
        float temperature_c = ((Vsense - 0.76f) / 0.0025f) + 25.0f;

        // ---- Store in filter buffer ----
        temp_buffer[temp_index++] = temperature_c;
        if (temp_index >= FILTER_SIZE)
            temp_index = 0;

        // ---- Compute moving average ----
        float sum = 0;
        for (int i = 0; i < FILTER_SIZE; i++)
            sum += temp_buffer[i];

        float filtered_temp = sum / FILTER_SIZE;

        // ---- Convert float to int for printing ----
        int temp_int = (int)filtered_temp;


        // ---- Format UART message ----
        len = sprintf(msg, "TEMP: %d\r\n", temp_int);

        // ---- Send to Raspberry Pi ----
        HAL_UART_Transmit(&huart1, (uint8_t*)msg, len, HAL_MAX_DELAY);
        // ---- Simple memory telemetry ----
        char mem_msg[40];
        int fake_heap = 1024;   // simulated value (safe for now)

        sprintf(mem_msg, "MEM_FREE: %d\r\n", fake_heap);
        HAL_UART_Transmit(&huart1, (uint8_t*)mem_msg, strlen(mem_msg), HAL_MAX_DELAY);


        HAL_Delay(1000);
    }
}

// DO NOT MODIFY – CubeMX generated clock config
void SystemClock_Config(void)
{
    RCC_OscInitTypeDef RCC_OscInitStruct = {0};
    RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};

    __HAL_RCC_PWR_CLK_ENABLE();
    __HAL_PWR_VOLTAGESCALING_CONFIG(PWR_REGULATOR_VOLTAGE_SCALE2);

    RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSI;
    RCC_OscInitStruct.HSIState = RCC_HSI_ON;
    RCC_OscInitStruct.HSICalibrationValue = RCC_HSICALIBRATION_DEFAULT;
    RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
    RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSI;
    RCC_OscInitStruct.PLL.PLLM = 16;
    RCC_OscInitStruct.PLL.PLLN = 336;
    RCC_OscInitStruct.PLL.PLLP = RCC_PLLP_DIV4;
    RCC_OscInitStruct.PLL.PLLQ = 7;

    if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
    {
        Error_Handler();
    }

    RCC_ClkInitStruct.ClockType =
        RCC_CLOCKTYPE_HCLK |
        RCC_CLOCKTYPE_SYSCLK |
        RCC_CLOCKTYPE_PCLK1 |
        RCC_CLOCKTYPE_PCLK2;

    RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
    RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
    RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
    RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

    if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
    {
        Error_Handler();
    }
}

void Error_Handler(void)
{
    __disable_irq();
    while (1) { }
}
