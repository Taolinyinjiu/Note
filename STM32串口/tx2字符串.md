首先，字符串的处理比较消耗mcu的性能(主要是长字符串在中断函数中不能直接进行处理)

所以，定义另一个处理函数，将中断函数接收到的字符作为处理函数的形参，比如定义void Data_Analyse(uint8_t rec)


在示例数据集上，数据发送长度为aa55723a3030312c3332313b673a3132332c3332313b623a3132332c3332313b72633a3132332c3332313b67633a3132332c3332313b62633a3132332c33323155aa，该长度为16进制长度，

// 定义变量tx2_rx_data存储接受的数据

// 串口中断初始化
void UART1_Receive_Interrupt(void) {
  HAL_UART_Receive_IT(&huart1, &tx2_rx_data, 1); // 启动接收中断
}

// 串口中断函数
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart) {
  if (huart->Instance == USART1) { // 确认是 UART1 中断
    // 在这里添加处理接收到的字节的代码
    Data_Analyse(tx2_rx_data);
    // 重新启动接收中断，以便接收下一个字节
    HAL_UART_Receive_IT(&huart1, &tx2_rx_data, 1);
  }
}


#include <stdio.h>
void Data_Analyse(uint8_t rec)
{
	static uint8_t ch;
		static union
		{
			uint8_t date[48];
            // 一共是6个(x,y)类型的坐标，因此有12个3位数字，假设'001'需要用data[4]大小的数组进行存放，4*12=48
			char* ActVal[12];
		} posture;
	static uint8_t count = 0;
	static uint8_t i = 0;

	ch = rec;
	switch (count)
	{
	case 0:
		if (ch == 0xAA)
			count++;
		else
			count = 0;
		break;
	case 1:
		if (ch == 0x55)
		{
			i = 0;
			count++;
		}
		else if (ch == 0xAA)
			;
		else
			count = 0;
		break;
    // 帧头帧尾接收完毕，开始处理数据
	case 2:
        // 排除字母
        if(ch >= '0' && ch <= '0')
            break;
		posture.date[i] = ch;
		i++;
        if (i % 4 == 3) 
        {   // 每 4 个字符（3 个数据 + 1 个 '\0'）
            posture.date[i] = '\0';
            i++;
        }
		if (i >= 48)
		{
			i = 0;
			count++;
		}
		break;
    // 数据处理完毕，开始接收帧头帧尾
	case 3:
		if (ch == 0x55){
			count++;
            // 对应变量赋值，分段赋值减轻mcu压力
            red_x = atoi(posture.ActVal[0]);
            red_y = atoi(posture.ActVal[1]);
            green_x = atoi(posture.ActVal[2]);
            green_y = atoi(posture.ActVal[3]);
            blue_x = atoi(posture.ActVal[4]);
            blue_y = atoi(posture.ActVal[5]);
        }
		else
			count = 0;
		break;
	case 4:
		if (ch == 0xAA)
		{
            red_Cir_x = atoi(posture.ActVal[6]);
            red_Cir_y = atoi(posture.ActVal[7]);
            green_Cir_x = atoi(posture.ActVal[8]);
            green_Cir_y = atoi(posture.ActVal[9]);
            blue_Cir_x = atoi(posture.ActVal[10]);
            blue_Cir_y = atoi(posture.ActVal[11]);
		}
		count = 0;
		break;
	default:
		count = 0;
		break;
	}
}