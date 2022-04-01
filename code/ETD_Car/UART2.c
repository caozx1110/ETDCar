/*
 * UART2.c
 *
 *  Created on: 2021Äê7ÔÂ1ÈÕ
 *      Author: q7423
 */

#include "UART2.h"

#define FIFOSIZE2   256       // size of the FIFOs (must be power of 2)
#define FIFOSUCCESS2 1        // return value on success
#define FIFOFAIL2    0        // return value on failure
uint32_t RxPutI2;      // should be 0 to SIZE-1
uint32_t RxGetI2;      // should be 0 to SIZE-1
uint32_t RxFIFO2Lost2;  // should be 0
uint8_t RxFIFO2[FIFOSIZE2];
void RxFIFO2_Init(void){
  RxPutI2 = RxGetI2 = 0;                      // empty
  RxFIFO2Lost2 = 0; // occurs on overflow
}
int RxFIFO2_Put(uint8_t data){
  if(((RxPutI2+1)&(FIFOSIZE2-1)) == RxGetI2){
    RxFIFO2Lost2++;
    return FIFOFAIL2; // fail if full
  }
  RxFIFO2[RxPutI2] = data;                    // save in FIFO
  RxPutI2 = (RxPutI2+1)&(FIFOSIZE2-1);         // next place to put
  return FIFOSUCCESS2;
}
int RxFIFO2_Get(uint8_t *datapt){
  if(RxPutI2 == RxGetI2) return 0;            // fail if empty
  *datapt = RxFIFO2[RxGetI2];                 // retrieve data
  RxGetI2 = (RxGetI2+1)&(FIFOSIZE2-1);         // next place to get
  return FIFOSUCCESS2;
}

//------------UART2_InStatus------------
// Returns how much data available for reading
// Input: none
// Output: number of bytes in receive FIFO
uint32_t UART2_InStatus(void){
 return ((RxPutI2 - RxGetI2)&(FIFOSIZE2-1));
}
//------------UART2_Init------------
// Initialize the UART for 115,200 baud rate (assuming 12 MHz SMCLK clock),
// 8 bit word length, no parity bits, one stop bit
// Input: none
// Output: none
void UART2_Init(void){
  RxFIFO2_Init();              // initialize FIFOs
  EUSCI_A1->CTLW0 = 0x0001;         // hold the USCI module in reset mode
  // bit15=0,      no parity bits
  // bit14=x,      not used when parity is disabled
  // bit13=0,      LSB first
  // bit12=0,      8-bit data length
  // bit11=0,      1 stop bit
  // bits10-8=000, asynchronous UART mode
  // bits7-6=11,   clock source to SMCLK
  // bit5=0,       reject erroneous characters and do not set flag
  // bit4=0,       do not set flag for break characters
  // bit3=0,       not dormant
  // bit2=0,       transmit data, not address (not used here)
  // bit1=0,       do not transmit break (not used here)
  // bit0=1,       hold logic in reset state while configuring
  EUSCI_A1->CTLW0 = 0x00C1;
                              // set the baud rate
                              // N = clock/baud rate = 12,000,000/115,200 = 104.1667
  EUSCI_A1->BRW = 104;        // UCBR = baud rate = int(N) = 104

  EUSCI_A1->MCTLW = 0x0000;   // clear first and second modulation stage bit fields
// since TxFifo is empty, we initially disarm interrupts on UCTXIFG, but arm it on OutChar
  P2->SEL0 |= 0x0C;
  P2->SEL1 &= ~0x0C;          // configure P2.3 and P2.2 as primary module function
  NVIC->IP[4] = (NVIC->IP[4]&0xFF00FFFF)|0x00400000; // priority 2
  NVIC->ISER[0] = 0x00020000; // enable interrupt 18 in NVIC
  EUSCI_A1->CTLW0 &= ~0x0001; // enable the USCI module
                              // enable interrupts on receive full
  EUSCI_A1->IE = 0x0001;      // disable interrupts on transmit empty, start, complete
}


//------------UART2_InChar------------
// Wait for new serial port input, interrupt synchronization
// Input: none
// Output: an 8-bit byte received
// spin if RxFIFO2 is empty
uint8_t UART2_InChar(void){
  uint8_t letter;
  while(RxFIFO2_Get(&letter) == FIFOFAIL2){};
  return(letter);
}

///------------UART2_OutChar------------
// Output 8-bit to serial port, busy-wait
// Input: letter is an 8-bit data to be transferred
// Output: none
void UART2_OutChar(uint8_t data){
  while((EUSCI_A1->IFG&0x02) == 0);
  EUSCI_A1->TXBUF = data;
}
// interrupt 18 occurs on :
// UCRXIFG RX data register is full
// vector at 0x00000088 in startup_msp432.s
void EUSCIA1_IRQHandler(void){
  if(EUSCI_A1->IFG&0x01){             // RX data register full
    RxFIFO2_Put((uint8_t)EUSCI_A1->RXBUF);// clears UCRXIFG
  }
}

//------------UART2_OutString------------
// Output String (NULL termination)
// Input: pointer to a NULL-terminated string to be transferred
// Output: none
void UART2_OutString(uint8_t *pt){
  while(*pt){
    UART2_OutChar(*pt);
    pt++;
  }
}
//------------UART2_FinishOutput------------
// Wait for all transmission to finish
// Input: none
// Output: none
void UART2_FinishOutput(void){
  // Wait for entire tx message to be sent
  while((EUSCI_A1->IFG&0x02) == 0);
}
