/*
 * PID.h
 *
 *  Created on: 2021��7��2��
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

//ȫ�ֱ���

#define HIGHSPEED       8000
#define MIDSPEED        5000
#define LOWSPEED        3000

//��������ϵ��
#define FB 10

//ֱ��Ȧ����ƫ,Ŀ�����ȥ��ֵ
#define CIRCLEREPAIR 0.42

//ת����ƫ
#define TURNREPAIR 17

extern float INIT_ANGLE;
extern float TARGET_ANGLE;

//ǰ��
void PID_Forward(int Speed, float Distance);

//ת��
void PID_Turn(int Speed, float Angle);

float Ang1SubAng2(float Ang1, float Ang2);
float Ang1AndAng2(float Ang1, float Ang2);

//��ȡ��ǰ�Ƕ���Ŀ��ǶȵĲ�ֵ


#endif /* PID_H_ */
