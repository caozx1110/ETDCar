/****
JY61.h
接口函数：
初始化函数（JY61_Init），实时更新角度和角速度数组
获取角度函数（Get_Angular），获得角度
Created on: 2021年7月1日
Author: mcl
******/

#ifndef JY61_H_
#define JY61_H_

#include "msp.h"
#include "UART2.h"
#include "Clock.h"
#include "UART0.h"

#define DATAHEAD        0x55     //包头校验位
#define ISANGLE         0x53     //角度包校验位
#define ISANGLESPEED    0x52     //角速度包校验位
#define bool            int

//uint8_t angular_speed[8];          //存放角速度包
//uint8_t angular[8];                //存放角度包
//uint8_t sum;                       //计算累加值

//初始化
void JY61_Init();

//获取角度
bool JY61_GetAngle(uint8_t* AngleZ);

//返回角度
float JY61_ReturnAngle();

#endif /* JY61_H_ */
