import string
def str2hex(stringApdu):
	temp = []

	if len(stringApdu)%2 == 0:
		for i in range(0,len(stringApdu),2):
			temp.append(string.atoi(('0x' + stringApdu[i:i+2]),16))
		return temp
			
	else:
		return 0

def hex2str(hexApdu):
	temp = ''
	for i in hexApdu:
		j = hex(i)
		j = j[2:]
		if len(j)<2:
			j = '0' + j
		temp += j
	return temp
				
def LV(data):
	lv = hex(len(data)//2)
	lv = lv[2:]
	if len(lv)<2:
		lv = '0' + lv
		
	return lv

	
	
