numberValue = 4342562935698728
checksum = 0;
count = 0
while(numberValue > 1):
	count += 1
	
	
	modulus = numberValue%10;
		
	if (count%2 == 0):
		modulus = modulus*2;
			
		if (modulus>9):
			innerModulus = modulus%10;
			modulus = modulus/10;
			modulus = modulus + innerModulus;
				
	checksum += modulus;
		
	numberValue = numberValue/10;
	print checksum
	

