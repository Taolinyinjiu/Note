sum = 0;
		sum_error = 0;
		solid_avg = 0;
		solid_error = 0;

		for(;channel<Solid_Number;channel++)
		{
			soil_humidity_adc[channel] = HW390_GetValue(channel);//��ȡ�� channel ������ʪ�ȴ�����������
		}
		
		// TODO: �����õ���ADCֵת��Ϊʪ��ֵ
		for(channel = 0;channel<(uint8_t)Solid_Number;channel++)
		{
			// ���Ƚ�ADC��ֵ����׼���õ�����
			soil_humidity[channel] = soil_humidity_adc[channel]; 
			// �����ж������޷�
			if(soil_humidity[channel] > Dry_ADC_Value)
				soil_humidity[channel] = Dry_ADC_Value; // 0%
			else if (soil_humidity[channel] < Wet_ADC_Value)
				soil_humidity[channel] = Wet_ADC_Value; // 100%
			
			// ���Ի�����ADCֵ��ʪ��%���ж�Ӧ
			soil_humidity[channel] = ( 1 - ((soil_humidity[channel] - Wet_ADC_Value) / (Dry_ADC_Value - Wet_ADC_Value))) * 100;
			// ��ͣ�Ϊ�������˹��ɭϵ����׼��
			sum += soil_humidity[channel];
		}
		
		// ����ƽ��ֵ
		solid_avg = sum/(Solid_Number);
		
		// ���㷽��
		for(channel = 0;channel<(uint8_t)Solid_Number;channel++)
		{
			// ����ÿ������ֵͬƽ��ֵ�Ĳ�ֵ
			solid_error = soil_humidity[channel] -  solid_avg;
			// ȡ����ֵ
			if(solid_error < 0)
				solid_error = -solid_error;
			// ������
			sum_error += (solid_error / soil_humidity[channel]);
		}
		// �������˹��ɭϵ�����������ι���ȶ�
//		Christ = (1 - (sum_error/10) ) * 100;	