sum = 0;
		sum_error = 0;
		solid_avg = 0;
		solid_error = 0;

		for(;channel<Solid_Number;channel++)
		{
			soil_humidity_adc[channel] = HW390_GetValue(channel);//获取第 channel 个土壤湿度传感器的数据
		}
		
		// TODO: 将检测得到的ADC值转换为湿度值
		for(channel = 0;channel<(uint8_t)Solid_Number;channel++)
		{
			// 首先将ADC的值赋给准备好的数组
			soil_humidity[channel] = soil_humidity_adc[channel]; 
			// 接着判断上下限幅
			if(soil_humidity[channel] > Dry_ADC_Value)
				soil_humidity[channel] = Dry_ADC_Value; // 0%
			else if (soil_humidity[channel] < Wet_ADC_Value)
				soil_humidity[channel] = Wet_ADC_Value; // 100%
			
			// 线性化，将ADC值与湿度%进行对应
			soil_humidity[channel] = ( 1 - ((soil_humidity[channel] - Wet_ADC_Value) / (Dry_ADC_Value - Wet_ADC_Value))) * 100;
			// 求和，为计算克里斯琴森系数做准备
			sum += soil_humidity[channel];
		}
		
		// 计算平均值
		solid_avg = sum/(Solid_Number);
		
		// 计算方差
		for(channel = 0;channel<(uint8_t)Solid_Number;channel++)
		{
			// 计算每个测量值同平均值的差值
			solid_error = soil_humidity[channel] -  solid_avg;
			// 取绝对值
			if(solid_error < 0)
				solid_error = -solid_error;
			// 误差求和
			sum_error += (solid_error / soil_humidity[channel]);
		}
		// 计算克里斯琴森系数表征土壤滴灌均匀度
//		Christ = (1 - (sum_error/10) ) * 100;	