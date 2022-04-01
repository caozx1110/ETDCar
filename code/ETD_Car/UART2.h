/*
 * UART2.h
 *
 *  Created on: 2021Äê7ÔÂ1ÈÕ
 *      Author: q7423
 */

#ifndef UART2_H_
#define UART2_H_

#include <stdint.h>
#include "msp.h"

// standard ASCII symbols
/**
 * \brief Carriage return character
 */
#define CR   0x0D
/**
 * \brief Line feed character
 */
#define LF   0x0A
/**
 * \brief Back space character
 */
#define BS   0x08
/**
 * \brief escape character
 */
#define ESC  0x1B
/**
 * \brief space character
 */
#define SP   0x20
/**
 * \brief delete character
 */
#define DEL  0x7F

/**
 * @details   Initialize EUSCI_A2 for UART operation
 * @details   115,200 baud rate (assuming 12 MHz SMCLK clock),
 * @details   8 bit word length, no parity bits, one stop bit
 * @param  none
 * @return none
 * @brief  Initialize EUSCI A2
 */
void UART2_Init(void);

/**
 * @details   Receive a character from EUSCI_A2 UART
 * @details   Interrupt synchronization,
 * @details   blocking, spin if RxFifo is empty
 * @param  none
 * @return ASCII code of received data
 * @note   UART2_Init must be called once prior
 * @brief  Receive byte into MSP432
 */
uint8_t UART2_InChar(void);

/**
 * @details   Transmit a character to EUSCI_A2 UART
 * @details   Busy-wait synchronization,
 * @details   blocking, wait for UART to be ready
 * @param  data is the ASCII code for data to send
 * @return none
 * @note   UART2_Init must be called once prior
 * @brief  Transmit byte out of MSP432
 */
void UART2_OutChar(uint8_t data);

/**
 * @details   Transmit a string to EUSCI_A2 UART
 * @param  pt is pointer to null-terminated ASCII string to be transferred
 * @return none
 * @note   UART2_Init must be called once prior
 * @brief  Transmit string out of MSP432
 */
void UART2_OutString(uint8_t *pt);


/**
 * @details   Wait for all transmission to finish
 * @details   Busy-wait synchronization,
 * @details   blocking, wait for all UART output to be finished
 * @param  none
 * @return none
 * @brief  wait for UART output to complete
 */
void UART2_FinishOutput(void);


/**
 * @details   Check the receive FIFO from EUSCI_A2 UART
 * @details   non-blocking
 * @param  none
 * @return number of characters in FIFO available for reading
 * @brief  Check status of receive FIFO
 */
uint32_t UART2_InStatus(void);

#endif /* UART2_H_ */
