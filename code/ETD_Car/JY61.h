/****
JY61.h
�ӿں�����
��ʼ��������JY61_Init����ʵʱ���½ǶȺͽ��ٶ�����
��ȡ�ǶȺ�����Get_Angular������ýǶ�
Created on: 2021��7��1��
Author: mcl
******/

#ifndef JY61_H_
#define JY61_H_

#include "msp.h"
#include "UART2.h"
#include "Clock.h"
#include "UART0.h"

#define DATAHEAD        0x55     //��ͷУ��λ
#define ISANGLE         0x53     //�ǶȰ�У��λ
#define ISANGLESPEED    0x52     //���ٶȰ�У��λ
#define bool            int

//uint8_t angular_speed[8];          //��Ž��ٶȰ�
//uint8_t angular[8];                //��ŽǶȰ�
//uint8_t sum;                       //�����ۼ�ֵ

//��ʼ��
void JY61_Init();

//��ȡ�Ƕ�
bool JY61_GetAngle(uint8_t* AngleZ);

//���ؽǶ�
float JY61_ReturnAngle();

#endif /* JY61_H_ */
