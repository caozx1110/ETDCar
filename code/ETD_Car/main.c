#include "HC05.h"
//#include "Infrared.h"
/**
 * 蓝牙控制运动
 */

void main(void)
{
    Clock_Init48MHz();
    UART0_Initprintf();
    HC05_Init();
    JY61_Init();
    Tachometer_Init();
    Infrared_Init();
//    int Speed = 4000;
//    uint16_t LeftTach, RightTach;
//    int32_t LeftSteps, RightSteps;
//    enum TachDirection LeftDir, RightDir;
//    uint8_t AngleZHL[2];
//    float DeltaAngle = 0;
//    float AngleZ;

    Clock_Delay1ms(1000);
    INIT_ANGLE = JY61_ReturnAngle();
    //Clock_Delay1ms(1000);

	while(1)
	{
	    //Motor_Forward(5000, 5000);
	    //PID_Forward(MIDSPEED, 10);
	    //PID_Turn(LOWSPEED, 90);
	    HC05_Motor();
	    //printf("%d\n", Infrared_Get());

	    //HC05_UselessMotor();
//	    HC05_Motor();
//	    DeltaAngle = JY61_ReturnAngle();
//	    DeltaAngle = (DeltaAngle - InitAngle) >= 0 ? (DeltaAngle - InitAngle) : (DeltaAngle - InitAngle + 360);
//	    HC05_AngleToBit8(DeltaAngle, AngleZHL);
//	    HC05_SendChar(AngleZHL[0]);     //高位
//	    HC05_SendChar(AngleZHL[1]);     //低位
//	    printf("%.1f %d %d\n", DeltaAngle, AngleZHL[0], AngleZHL[1]);
	    //Clock_Delay1ms(1000);

	    //测试直行
//	    Tachometer_Get(&LeftTach, &LeftDir, &LeftSteps, &RightTach, &RightDir, &RightSteps);
//	    printf("%d\n", LeftTach);
//	    uint8_t temp[2];
//	    UART1_OutString(Bit16toBit8(LeftTach, temp));
//	    UART1_OutString(Bit16toBit8(RightTach, temp));
//	    Bit16toBit8(LeftTach, temp);
//	    UART1_OutChar(temp[0]);
//	    UART1_OutChar(temp[1]);
	    //UART1_OutString(&LeftSteps);
//	    Bit16toBit8(RightTach, temp);
//	    UART1_OutChar(temp[0]);
//	    UART1_OutChar(temp[1]);
	    //UART1_OutString(&RightSteps);

	}
}
