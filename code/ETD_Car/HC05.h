/*
 * HC05.h
 *
 *  Created on: 2021年7月1日
 *      Author: q7423
 */

#ifndef HC05_H_
#define HC05_H_

#include "PID.h"
#include "Infrared.h"
#include "LittleStar.h"

#define FORWARD         'F'
#define BACKWARD        'B'
#define LEFTWARD        'L'
#define RIGHTWARD       'R'
#define STOP            'S'
#define HIGHSPEEDLEVEL  'h'
#define MIDSPEEDLEVEL   'm'
#define LOWSPEEDLEVEL   'l'

//初始化
void HC05_Init();

//蓝牙发送uint8_t
void HC05_SendChar(uint8_t Data);

//蓝牙发送数组
void HC05_SendString(uint8_t* Data);

//电脑给出方向、速度等级、运动时间
void HC05_Motor();

//电脑给出方向
void HC05_UselessMotor();

//十六位int转成8位int数组
uint8_t* HC05_Bit16toBit8(uint16_t word_16, uint8_t* point_8);

//32位int转成8位int数组
uint8_t* HC05_Bit32toBit8(uint32_t word_32, uint8_t* point_8);

void HC05_AngleToBit8(float Angle, uint8_t* AngleHL);

#endif /* HC05_H_ */
