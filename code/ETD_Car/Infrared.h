/*
 * Infrared.h
 *
 *  Created on: 2021年7月7日
 *      Author: mcl
 */

#ifndef INFRARED_H_
#define INFRARED_H_

#include "msp.h"

//初始化端口函数
void Infrared_Init(void);
//检测是否出现障碍
int Infrared_Get(void);
#endif /* INFRARED_H_ */
