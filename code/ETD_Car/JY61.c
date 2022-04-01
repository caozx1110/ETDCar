#include "JY61.h"

//初始化
void JY61_Init()
{
    UART2_Init();
}

//获取角度，AngleZ[2]
bool JY61_GetAngle(uint8_t* AngleZ)
{
    uint8_t Buffer[8];  //缓存
    uint8_t Sum = 0;    //总和校验
    uint8_t Receive;    //接受数据
    uint8_t i;

    RxFIFO2_Init();
    while (1)
    {
        Receive = UART2_InChar();
        if (Receive == DATAHEAD)
        {
            Sum = Receive;  //初始化校验位
            Receive = UART2_InChar();
            if (Receive == ISANGLESPEED)
            {
                Sum += Receive;
                for (i = 0; i < 8; i++)
                {
                    Buffer[i] = UART2_InChar();
                    Sum += Buffer[i];
                }
                Receive = UART2_InChar();
                if (Receive == Sum)
                {
//                  for(i = 0; i < 8; i++)
//                  {
//                      angular_speed[i] = Buffer[i];
//                  }
                }
            }
            else if (Receive == ISANGLE)
            {
                Sum += Receive;
                for (i = 0; i < 8; i++)
                {
                    Buffer[i] = UART2_InChar();
                    Sum += Buffer[i];
                }
                Receive = UART2_InChar();
                if (Receive == Sum)
                {
                    //printf("%d %d\n", Buffer[5], Buffer[4]);
                    AngleZ[1] = Buffer[4];  //低位
                    AngleZ[0] = Buffer[5];  //高位
                    return 1;
                }
            }
        }
    }

}

float JY61_ReturnAngle()
{
    uint8_t AngleZHL[2];
    float AngleZ;

    if (JY61_GetAngle(AngleZHL))
    {
        AngleZ = (AngleZHL[0] * 256 + AngleZHL[1]) * 1800 / 32768;
        AngleZ /= 10;
        return AngleZ;
    }

    return 0;
}
