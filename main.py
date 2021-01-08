#bin/bash/python3
import os
import argparse
import sys

def generateBit(n):
    byts = os.urandom(n)
    bits = ''
    count = 0
    for i in bytearray(byts):
        byte = bin(i)[2:]
        if len(byte) < 8:
            zeros = ''
            dif = 8 - len(byte) 
            for j in range(dif):
                zeros += '0'
            byte = zeros + byte
        bits += byte
    return bits


#generateBitStream(48) #384 bits 
#generateBitStream(250) 2000 bytes 

def GenerateKeyPath(dirPath):

    if not os.path.exists(dirPath):
        os.makedirs(dirPath)
    
    count = 0
    fileDir = os.path.join(dirPath, '0000')

    while os.path.exists(fileDir):
        count += 1
        fileDir = os.path.join(dirPath, str(count).rjust(4, '0'))    
    os.makedirs(fileDir) 
    
    count2 = 0
    while count2 < 100:
    	f = os.path.join(fileDir, str(count2).rjust(2, '0'))
    	file1 = f+'p.txt'
    	file2 = f+'s.txt'
    	file3 = f+'c.txt'
    	count2 +=1
    	fileP = open(file1, "w")
    	fileP.write(generateBit(48))
    	fileP.close()
    	fileC = open(file2, "w")
    	fileC.write(generateBit(48))
    	fileC.close()
    	fileS = open(file3, "w")
    	fileS.write(generateBit(2000))
    	fileS.close()
        

def Get_cipher_for_encode (dir):


    dirPath = os.path.join(dir, '0000')
    number_folder = 0
    number_cipher = 0
    while not os.path.exists(dirPath):
        number_folder += 1
        dirPath = os.path.join(dir, str(number_folder).rjust(4, '0'))

    for x in range(100):
        cfile = '{0:02}'.format(x)+'c.txt'
        pfile = '{0:02}'.format(x)+'p.txt'
        sfile = '{0:02}'.format(x)+'s.txt'

        Bool =  os.path.isfile(os.path.join(dirPath, cfile))
        Bool2 =  os.path.isfile(os.path.join(dirPath, pfile))
        Bool3 =  os.path.isfile(os.path.join(dirPath, sfile))

        if Bool and Bool2 and Bool3:
        	cipher = os.path.join(dirPath, cfile)
        	prefix = os.path.join(dirPath, pfile)
        	sufix = os.path.join(dirPath, sfile)
        	break
   
    return cipher, prefix, sufix





def convertTOBunery(text):
    '''
    :param text:
    :return: !binnary
    using join() + ord() + format()
    Converting String to binary
    binnary : return the binary value
    '''
    binnary = ''.join(format(ord(i), 'b').rjust(8,"0") for i in text)
    return binnary



def Send_Cipher(text, cipher,p,s):



	FC = open(cipher, "r")
	cipher2 = FC.read()
	FP = open(p, "r")
	prefix = FP.read()
	FS = open(s, "r")
	suffix = FS.read()
	FP.close()
	FC.close()
	FS.close()


	c = ''
	if len(text) > len(cipher2):
		print ('Error text to long than key')
		exit()
	for i in range(len(text)):
		a = int(text[i])
		b = int(cipher2[i])
		tmp = a^b
		c += str(tmp)
	path = cipher.split(os.sep)

	path = '' + path[0] + '-' + path[1] + '-' + path[2].replace('c','t')

	f_ = open(path, "w")
	f_.write(prefix + c + suffix)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("-g", '--generate', action='store_true')
	parser.add_argument("-s", '--send', action='store_true')
	parser.add_argument("-f", '--file',)
	parser.add_argument("-t", '--text')
	parser.add_argument('folder')
	args = parser.parse_args()
	if (args.send):
		if args.file:
			text = args.file
			with open(args.file, 'r') as file:
				text = file.read()

		elif args.text:
			text = args.text

		else:
			text = input("Enter your text please! : ")
		texte_bennary = convertTOBunery(text)
		cipher, p, s = Get_cipher_for_encode(args.folder)
		Send_Cipher(texte_bennary,cipher, p, s)

	else:
		GenerateKeyPath(args.folder)
