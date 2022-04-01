/*
 * Infrared.c
 *
 *  Created on: 2021��7��7��
 *      Author: q7423
 */

#include "Infrared.h"

//��ʼ���˿ں���
void Infrared_Init(void){
    P2 -> SEL0 &= ~0x20;
    P2 -> SEL1 &= ~0x20;   //configure P2.5 as GPIO
    P2 -> DIR  &= ~0x20;   //make P2.5 in
}
//����Ƿ�����ϰ�
int Infrared_Get(void){
    return P2 -> IN & 0x20;
}

