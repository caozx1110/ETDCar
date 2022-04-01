/*
 * HC05.h
 *
 *  Created on: 2021��7��1��
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

//��ʼ��
void HC05_Init();

//��������uint8_t
void HC05_SendChar(uint8_t Data);

//������������
void HC05_SendString(uint8_t* Data);

//���Ը��������ٶȵȼ����˶�ʱ��
void HC05_Motor();

//���Ը�������
void HC05_UselessMotor();

//ʮ��λintת��8λint����
uint8_t* HC05_Bit16toBit8(uint16_t word_16, uint8_t* point_8);

//32λintת��8λint����
uint8_t* HC05_Bit32toBit8(uint32_t word_32, uint8_t* point_8);

void HC05_AngleToBit8(float Angle, uint8_t* AngleHL);

#endif /* HC05_H_ */
