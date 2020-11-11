import smbus



if __name__ == "__main__":
	msg = str(hex(int(float(1)/10*32000)))
	print(msg)
	print(len(msg))
	msg = msg.replace('0x', '')
	print(('0'+msg).upper())
	print(len(msg))