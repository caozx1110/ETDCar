#include "PID.h"

float INIT_ANGLE = 0;
float TARGET_ANGLE = 0;

//Ang1���Ang2�ĽǶȣ���˳ʱ��Ϊ�������0~360
float Ang1SubAng2(float Ang1, float Ang2)
{
    float Delta = Ang1 - Ang2;
    while (Delta < 0)
    {
        Delta += 360;
    }
    while (Delta > 360)
    {
        Delta -= 360;
    }
    return Delta;
}

float Ang1AndAng2(float Ang1, float Ang2)
{
    float Delta = Ang1 + Ang2;
    while (Delta < 0)
    {
        Delta += 360;
    }
    while (Delta > 360)
    {
        Delta -= 360;
    }
    return Delta;
}

//DistanceΪȦ��
void PID_Forward(int Speed, float Distance)
{
    int leftDuty, rightDuty;
    leftDuty  = Speed;
    rightDuty = Speed - 100;
    int InitStep = Tachometer_GetStep();    //��ʼ����
    float InitAngle = JY61_ReturnAngle();   //��ʼ�Ƕ�
    float AngleT;
    float CurAngle = 0;
    Distance -= CIRCLEREPAIR;

    while(Tachometer_GetStep() - InitStep < Distance * 360)
    {
        CurAngle = Ang1SubAng2(JY61_ReturnAngle(), InitAngle);
        if(CurAngle > 1.0 && CurAngle < 90.0)        //��ƫ
        {
            rightDuty +=  FB * CurAngle;
        }
        else if(CurAngle < 359.0 && CurAngle > 270.0)  //��ƫ
        {
            rightDuty  -= FB * (360 - CurAngle);
        }
        Motor_Forward(leftDuty, rightDuty);
    }
    Motor_Stop();
    AngleT = Ang1SubAng2(JY61_ReturnAngle(), InitAngle);
    while ((AngleT > 0.5 && AngleT < 30) || (AngleT < 359.5 && AngleT > 330))
    {
        AngleT = Ang1SubAng2(JY61_ReturnAngle(), InitAngle);
        if (AngleT > 0.5 && AngleT < 30)
        {
            Motor_Left(5000, 5000);
            Clock_Delay1ms(40);
            Motor_Stop();
        }
        if (AngleT < 359.5 && AngleT > 330)
        {
            Motor_Right(5000, 5000);
            Clock_Delay1ms(40);
            Motor_Stop();
        }
    }
}

void PID_Turn(int Speed, float Angle)
{
    float InitAngle = JY61_ReturnAngle();
    int leftDuty, rightDuty;
    float AngleS;

    leftDuty  = Speed;
    rightDuty = Speed - 100;

    //��ת��˳ʱ��ת
    if (Angle > 0 && Angle <= 180)
    {
        Angle -= TURNREPAIR;
        Motor_Right(leftDuty, rightDuty);
        while(Ang1SubAng2(JY61_ReturnAngle(), InitAngle) < Angle)
        {
            Motor_Right(leftDuty, rightDuty);
        }
        Motor_Stop();
        Angle += TURNREPAIR;
        AngleS = Ang1SubAng2(JY61_ReturnAngle(), InitAngle) - Angle;
        while(AngleS > 0.5 || AngleS < -0.5){
            AngleS = Ang1SubAng2(JY61_ReturnAngle(), InitAngle) - Angle;
            if(AngleS > 0.5)
            {
                Motor_Left(5000, 5000);
                Clock_Delay1ms(40);
                Motor_Stop();
            }
            if(AngleS < -0.5)
            {
                Motor_Right(5000, 5000);
                Clock_Delay1ms(40);
                Motor_Stop();
            }
        }
    }
    else if (Angle > 180 && Angle < 360)
    {
        Angle += TURNREPAIR;
        Motor_Left(leftDuty, rightDuty);
        while(Ang1SubAng2(JY61_ReturnAngle(), InitAngle) > Angle)
        {
            Motor_Left(leftDuty, rightDuty);
        }
        Angle -= TURNREPAIR;
        AngleS = Ang1SubAng2(JY61_ReturnAngle(), InitAngle) - Angle;
        while(AngleS > 0.5 || AngleS < -0.5){
            AngleS = Ang1SubAng2(JY61_ReturnAngle(), InitAngle) - Angle;
            if(AngleS > 0.5)
            {
                Motor_Left(5000, 5000);
                Clock_Delay1ms(40);
                Motor_Stop();
            }
            if(AngleS < -0.5)
            {
                Motor_Right(5000, 5000);
                Clock_Delay1ms(40);
                Motor_Stop();
            }
        }
    }
}
