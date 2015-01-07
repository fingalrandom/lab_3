from PIL import Image, ImageDraw
ch = input('1. LSB \n2. Decode\n')
if ch == 1:
	nameIM = raw_input('Enter the name of container(*.jpg): ')
	inTXT = raw_input('Enter the name of text file(*.txt): ')
	rezIM = raw_input('Enter the name of result image(*.bmp): ')
	try:
		IM = Image.open(nameIM)
	except IOError:
		print('Image file not open')
		exit()
	sizeI = IM.size
	curWid = 0;	curHeig = 0
	try:
		f = open(inTXT, "r")
	except IOError:
		print('Text file not open')
		exit()
	TXT = f.read()
	TXTlen = len(TXT)
	hBit = []
	
	for i in range((TXTlen + 2) * 3):
		hBit.append([])
	hBit[0] = TXTlen >> 14
	hBit[1] = (TXTlen & 0b11100000000000) >> 11
	hBit[2] = (TXTlen & 0b11100000000) >> 8
	hBit[3] = (TXTlen & 0b11000000) >> 6
	hBit[4] = (TXTlen & 0b111000) >> 3
	hBit[5] = TXTlen & 0b111
	
	for id, cur in enumerate(TXT):
		hBit[(id + 2) * 3] = ord(cur) >> 6
		hBit[(id + 2) * 3 + 1] = (ord(cur) & 0b00111000) >> 3
		hBit[(id + 2) * 3 + 2] = ord(cur) & 0b00000111
	
	for i in range(TXTlen + 2):
		if curHeig >= sizeI[1]:
			curHeig = 0
			curWid = curWid + 1
			if curWid >= sizeI[0]:
				print("Not enough memory.")
				exit()
		px = IM.getpixel((curWid, curHeig))
		R = ((px[0] >> 2) << 2) + hBit[i * 3]
		G = ((px[1] >> 3) << 3) + hBit[i * 3 + 1]
		B = ((px[2] >> 3) << 3) + hBit[i * 3 + 2]
		IM.putpixel((curWid, curHeig), (R,G,B))
		curHeig = curHeig + 1
	IM.save(rezIM, "BMP")
	f.close()
elif ch == 2:
	nameIM = raw_input('Enter the name of container(*.bmp): ')
	rezTXT = raw_input('Enter the name of result file(*.txt): ')
	try:
		IM = Image.open(nameIM)
	except IOError:
		print('Image file not open')
		exit()
	height = IM.size[1]
	curWid = 0;	curHeig = 2
	pxAr = IM.load()
	tmp = ""
	
	td1 = pxAr[0,0][0] & 0b00000011
	td2 = pxAr[0,0][1] & 0b00000111
	td3 = pxAr[0,0][2] & 0b00000111
	lf = (td1 << 6) + (td2 << 3) + td3
	td1 = pxAr[0,1][0] & 0b00000011
	td2 = pxAr[0,1][1] & 0b00000111
	td3 = pxAr[0,1][2] & 0b00000111
	ls = (td1 << 6) + (td2 << 3) + td3
	TXTlen = lf * 256 + ls
	
	for i in range(TXTlen):
		if curHeig >= height:
			curHeig = 0
			curWid = curWid + 1
		td1 = pxAr[curWid, curHeig][0] & 0b00000011
		td2 = pxAr[curWid, curHeig][1] & 0b00000111
		td3 = pxAr[curWid, curHeig][2] & 0b00000111
		cur = chr((td1 << 6) + (td2 << 3) + td3)
		tmp = tmp + cur
		curHeig = curHeig + 1
	f = open(rezTXT, 'w')
	f.write(tmp)
	f.close()
else:
	print('Error! Irregular number.')
