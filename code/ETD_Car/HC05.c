/*
 * HC05.c
 *
 *  Created on: 2021年7月1日
 *      Author: q7423
 */

#include "HC05.h"



//十六位int转成8位int数组
uint8_t* HC05_Bit16toBit8(uint16_t word_16, uint8_t *point_8)
{
    point_8[1] = word_16 & 0xFF;
    point_8[0] = (word_16 >> 8) & 0xFF;
    return point_8;
}

//32位int转成8位int数组
uint8_t* HC05_Bit32toBit8(uint32_t word_32, uint8_t *point_8)
{
    point_8[3] = word_32 & 0xFF;
    point_8[2] = (word_32 >> 8) & 0xFF;
    point_8[1] = (word_32 >> 16) & 0xFF;
    point_8[0] = (word_32 >> 24) & 0xFF;
    return point_8;
}

//float Angle -> 八位数组
void HC05_AngleToBit8(float Angle, uint8_t* AngleHL)
{
    int temp = 0;
    temp = (int)(Angle * 32768 / 180);
    AngleHL[0] = temp / 256;
    AngleHL[1] = temp % 256;
}

//初始化
void HC05_Init()
{
    UART1_Init();
    Motor_Init();
}

//蓝牙发送uint8_t
void HC05_SendChar(uint8_t Data)
{
    UART1_OutChar(Data);
}

//蓝牙发送数组
void HC05_SendString(uint8_t* Data)
{
    UART1_OutString(Data);
}

//电脑给出角度、速度等级、运动距离
void HC05_Motor()
{
    uint8_t AngleH = UART1_InChar();
    //printf("%d", AngleH);
    uint8_t AngleL = UART1_InChar();
    //printf("%d", AngleL);
    uint8_t SpeedLevel = UART1_InChar();
    //printf("%c", SpeedLevel);
    uint8_t Distance = UART1_InChar();   //以0.1圈为单位，范围0~255
    //printf("%d", Distance);
    int Speed;
    int Angle = (AngleH * 256 + AngleL) * 180 / 32768;
    uint8_t AngleZHL[2];
    float DeltaAngle = 0;

    if (Angle > 44 && Angle < 46)
    {
        Angle = 270;
    }

    //选择速度
    switch(SpeedLevel)
    {
    case HIGHSPEEDLEVEL:
        Speed = HIGHSPEED;
        break;
    case MIDSPEEDLEVEL:
        Speed = MIDSPEED;
        break;
    case LOWSPEEDLEVEL:
        Speed = LOWSPEED;
        break;
    default:
        Speed = MIDSPEED;
        break;
    }
    //发送当前绝对角度
    DeltaAngle = JY61_ReturnAngle();
    DeltaAngle =
            (DeltaAngle - INIT_ANGLE) >= 0 ?
                    (DeltaAngle - INIT_ANGLE) : (DeltaAngle - INIT_ANGLE + 360);
    HC05_AngleToBit8(DeltaAngle, AngleZHL);
    HC05_SendChar (AngleZHL[0]);     //高位
    HC05_SendChar(AngleZHL[1]);     //低位

    if (Distance == 100)
    {
        MIDI_PLAY();
    }
    else
    {
        TARGET_ANGLE = Ang1AndAng2(TARGET_ANGLE, Angle);
        PID_Turn(LOWSPEED, Angle);
        if (Infrared_Get())
        {
            PID_Forward(Speed, Distance * 0.1);
            HC05_SendChar('E');
        }
        else
        {
            HC05_SendChar('C');
            Sound_Play();
        }
    }
//    //选择方向
//    switch (Direction)
//    {
//    case FORWARD:
//        //Motor_Forward(Speed, Speed);
//        PID_Forward(Speed, INIT_ANGLE, JY61_ReturnAngle());
//        break;
//    case BACKWARD:
//        Motor_Backward(Speed, Speed);
//        break;
//    case LEFTWARD:
//        Motor_Left(Speed, Speed);
//        break;
//    case RIGHTWARD:
//        Motor_Right(Speed, Speed);
//        break;
//    case STOP:
//        Motor_Stop();
//        break;
//    default:
//        Motor_Stop();
//        break;
//    }
//    //选择时间, 先改为1s
//    Clock_Delay1ms(RunTime * 1000);
}
//电脑给出方向
void HC05_UselessMotor()
{
    uint8_t Order = UART1_InChar();

    switch (Order)
    {
    case FORWARD:
        Motor_Forward(MIDSPEED, MIDSPEED);
        //PID_Forward(MIDSPEED, INIT_ANGLE, JY61_ReturnAngle());
        break;
    case BACKWARD:
        Motor_Backward(MIDSPEED, MIDSPEED);
        break;
    case LEFTWARD:
        Motor_Left(MIDSPEED, MIDSPEED);
        break;
    case RIGHTWARD:
        Motor_Right(MIDSPEED, MIDSPEED);
        break;
    case STOP:
        Motor_Stop();
        break;
    default:
        Motor_Stop();
        break;
    }
    //跑100ms
    Clock_Delay1ms(100);
}
