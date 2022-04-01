/****
LED.h
接口函数：LED_On(void);实现LED显示

Created on: 2021年6月29日
Author: mcl
******/
#ifndef LED_H_
#define LED_H_
//宏定义颜色
#define RED          0X01
#define GREEN        0X02
#define BLUE         0X04
#include "msp.h"
#include "Clock.h"

//初始化Port2引脚信息
void Port2_Init(void){
    P2 -> SEL0 &= ~0X13;
    P2 -> SEL1 &= ~0X13;   //configure P2.4 P2.1 P2.0 as GPIO
    P2 -> DS   |=  0X13;   //make P2.4 P2.1 P2.0 high drive strength
    P2 -> DIR  |=  0X13;   //make P2.4 P2.1 P2.0 out
    P2 -> OUT  &= ~0X13;   //LED all off
}

void Port2_Output(uint8_t data){
    P2 -> OUT = data;    //write all of P2 outputs
}

void LED_Off(void)
{
    P2 -> OUT &= ~0X13;
}

void LED_On(void)
{
    int i;
    Clock_Init48MHz();
    Port2_Init();
    for(i = 0;i < 5;i ++)
    {
        Port2_Output(RED);
        Clock_Delay1ms(100);
        Port2_Output(GREEN);
        Clock_Delay1ms(100);
        Port2_Output(BLUE);
        Clock_Delay1ms(100);
    }
    LED_Off();
}
#endif /* LED_H_ */
