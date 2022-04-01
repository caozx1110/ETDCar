/*
 * PID.h
 *
 *  Created on: 2021年7月2日
 *      Author: q7423
 */

#ifndef PID_H_
#define PID_H_

#include <stdio.h>
#include "msp.h"
#include "Clock.h"
#include "UART0.h"
#include "UART1.h"
#include "SysTick.h"
#include "LaunchPad.h"
#include "Tachometer.h"
#include "Motor.h"
#include "JY61.h"

//全局变量

#define HIGHSPEED       8000
#define MIDSPEED        5000
#define LOWSPEED        3000

//反馈比例系数
#define FB 10

//直行圈数修偏,目标需减去此值
#define CIRCLEREPAIR 0.42

//转弯修偏
#define TURNREPAIR 17

extern float INIT_ANGLE;
extern float TARGET_ANGLE;

//前进
void PID_Forward(int Speed, float Distance);

//转弯
void PID_Turn(int Speed, float Angle);

float Ang1SubAng2(float Ang1, float Ang2);
float Ang1AndAng2(float Ang1, float Ang2);

//获取当前角度与目标角度的差值


#endif /* PID_H_ */
