#!/usr/bin/env python
import sys

#Tarkistaa onko syotetty IP osoite validi ja oikeassa muodossa
def isIpValid(ip):
	octets = ip.split('.')
	#Tarkistetaan, etta osoitteessa varmasti 4 octettia jotka olivat erotettu pisteella. Eli validi DDN muoto
	if(len(octets)!=4):
		return False
	else:
		for octet in octets:
			#Tarkistetaan, etta oktetit sisaltavat vain numeroita
			if(not octet.isnumeric()):
				return False
			else:
				#Tarkistetaan, etta valideja numeroita
				if(int(octet) < 0 or int(octet) > 255):
					return False
	return True


#Tarkistaa onko syotetty maski validi ja oikeassa muodossa
def isMaskValid(mask):
	if(not mask.isnumeric()):
		return False
	else:
		#Tarkistetaan, etta sisaltaa vain valideja numeroita
		if(int(mask) < 1 or int(mask) > 32):
			return False
	return True


#Ottaa syotteen ja tarkistaa, etta se on oikeassa muodossa. Palauttaa taulukon jossa prefix ja maski
def getInput():
	syote = input("Syotä IP-osoite ja maski muodossa x.x.x.x/y: ")
	if '/' in syote:
		a = syote.split('/')
		#Tarkistetaan oikea muoto. Jos virheellinen niin lopetetaan
		if(isIpValid(a[0]) and isMaskValid(a[1])):
			return a
		else:
			print("Invalid IP-address")
			sys.exit()
	else:
		print("Invalid IP-address")
		sys.exit()


#Muuttaa IP Binaari muotoon.
def toBinary(ip):
	octets = ip.split('.')
	#octets taulukon jokainen octetti muutetaan 8 merkin pituiseksi binaariksi
	binaryIP = ['{0:08b}'.format(int(octet)) for octet in octets]
	return "".join(binaryIP)


#Palauttaa IP-osoitteen network osan binaarisena
def getNetworkBits(binaryAddress, mask):
	charArr = list(binaryAddress)
	prefix = []
	for x in range(mask):
		prefix.append(charArr[x])
	return prefix


def printAddress(prefix, mask, num):
	#Host bitteihin nollat tai ykköset, jotta saadaan pienin ja suurin osoite verkossa
	#Kaikki host bitit nollia = SubnetID
	#Kaikki host bitit ykkosia = Broadcast
	for x in range(mask-1, 31):
		prefix.append(num)
	binAddr = "".join(prefix)
	#Pilkkoo 32 merkkiä pitkän osoitteen 8 merkkisiksi ja laitetaan taulukkoon
	octets = [binAddr[i:i+8] for i in range(0, len(binAddr), 8)]
	#muutetaan stringit joissa binaari luvut kokonaisluvuiksi ja siitä tulostettavaksi
	ddn = []
	for octet in octets:
		ddn.append(str(int(octet, 2)))
	return ".".join(ddn)


#Printtaa maskin DDN muodossa ja /x muodossa
def printMask(mask):
	biMask = ""
	#Lisätään binaariseen maskiin maskin verran ykkosia ja loput nollia jotta saadaan validissa muodossa oleva maski
	for x in range(0, 32):
		if(x<mask):
			biMask += '1'
		else:
			biMask += '0'
	#Pilkkoo 32 merkkiä pitkän maskin 8 merkkisiksi ja laitetaan taulukkoon
	octets = [biMask[i:i+8] for i in range(0, len(biMask), 8)]
	#Muutetaan str muodossa olevat oktetit kokonaisluvuiksi ja tulostetaan maski DDN muodossa
	ddn = []
	for octet in octets:
		ddn.append(str(int(octet, 2)))
	print("Mask: " + ".".join(ddn) + " /"+ str(mask))


#Otetaan inputti ja testataan, että on oikeassa muodossa
address = getInput()
#Muutetaan IP-osoite binaari muotoon
binaryAddress = toBinary(address[0])
mask = int(address[1])
#Printataan maski eri muodoissa
printMask(mask)
#Printataan subnetID
prefix = getNetworkBits(binaryAddress, mask)
print("Subnet ID:", printAddress(prefix, mask, '0'))
#Printataan Broadcast address
prefix = getNetworkBits(binaryAddress, mask)
print("Broadcast:", printAddress(prefix, mask, '1'))