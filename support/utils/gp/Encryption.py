# -*- coding: utf-8 -*- 
from Crypto.Cipher import DES, DES3
from binascii import hexlify, unhexlify
from string import *
from operator import *
from array import *
from string import *

class Encryption:

    ## basic XOR and Not logic calc
    def SSC_Xor(self,inData1,inData2):
        outData = ''
        for i in range(0,len(inData1)):
            temp1 = inData1[i]
            temp2 = inData2[i]
            temp1 = int(temp1,16)
            temp2 = int(temp2,16)
            temp3 = str.upper(str(hex(temp1^temp2))[2:])
            outData = outData + temp3

        return outData
            
    def SSC_NOT(self,inData):
        outData = ''
        for i in range(0,len(inData)):
            temp1 = inData[i]
            temp1 = int(temp1,16)
            temp2 = upper(str(hex(15-temp1))[2:])
            outData = outData + temp2
        return outData
    
    ## basic Des: input(inData:string to calc,key:key to calc)
    def DES_Cipher_CBC(self, inData, DESKey):
        """Single Des Cipher CBC Mode"""
        inData=unhexlify(inData)
        DESKey=unhexlify(DESKey)
        obj=DES.new(DESKey, DES.MODE_CBC)
        outData=obj.encrypt(inData)
        outData=hexlify(outData)
        return outData.decode()
                
    def DES_Decipher_CBC(self, inData, DESKey):
        """Single Des Decipher CBC Mode"""
        inData=unhexlify(inData)
        DESKey=unhexlify(DESKey)
        obj=DES.new(DESKey, DES.MODE_CBC)
        outData=obj.decrypt(inData)
        outData=hexlify(outData)
        return outData.decode()
    
    def DES3_Cipher_CBC(self, inData, DES3Key):
        """Tri-Des Cipher CBC Mode"""
        inData=unhexlify(inData)
        DES3Key=unhexlify(DES3Key)
        obj=DES3.new(DES3Key, DES3.MODE_CBC )
        outData=obj.encrypt(inData)
        outData=hexlify(outData)
        return outData.decode()

    def DES3_Decipher_CBC(self, inData, DES3Key):
        """Tri-Des Decipher CBC Mode"""
        inData=unhexlify(inData)
        DES3Key=unhexlify(DES3Key)

        obj=DES3.new(DES3Key, DES3.MODE_CBC )
        outData=obj.decrypt(inData)
        outData=hexlify(outData)
        return outData.decode()  

    def DES3_Cipher_ECB(self,inData, DES3Key):
        """Tri-Des Cipher EBC Mode"""
        inData=unhexlify(inData)
        DES3Key=unhexlify(DES3Key)
        obj=DES3.new(DES3Key, DES3.MODE_ECB)
        outData=obj.encrypt(inData)
        outData=hexlify(outData)
        return outData.decode()

    def Data_Encrypt_DES3_CBC(self,random,inData,DESKey):
        inData=upper(inData)
        if len(inData)%16 == 0: 
            inData = inData+('8000000000000000')
        else:
            i = len(inData)%16
            k = 16-i
            inData = inData+'80'
            for j in range(1,k/2):
                inData = inData+'00'
        icv = unhexlify(random)
        inData = unhexlify(inData)
        DESKey = unhexlify(DESKey)
        obj = DES3.new(DESKey,DES3.MODE_CBC,icv)
        return hexlify(obj.encrypt(inData)).decode()
    
    def Data_Decrypt_DES3_CBC(self,random,inData,DESKey):
        icv = unhexlify(random)
        inData = unhexlify(inData)
        DESKey = unhexlify(DESKey)
        obj = DES3.new(DESKey,DES3.MODE_CBC,icv)
        ret = hexlify(obj.decrypt(inData))
        len = int(ret[:2],16)
        return ret.decode() 

    # calc Mac random:ICV ,inData :input string to calc,key:key to calc
    def MAC_SingleDESPlusTriDes_8Bytes(self, random, inData, DES3Key):
        """SingleDes Plus TriDes Mac calc .define in ISO9797-1 as MAC Algorithm3 with output transformation 3"""
        random = str.upper(random)
        inData = str.upper(inData)
        DES3Key = str.upper(DES3Key)
        if len(inData)%16 == 0: 
            inData = inData+('8000000000000000')
        else:
            i = len(inData)%16
            k = 16-i
            inData = inData+'80'
            for j in range(1,k//2):
                inData = inData+'00'
        sBlock = []
        for i in range(1,(len(inData)//16)+1):
            k = 16*(i-1)+1
            temp1 = inData[k-1:k+15]
            sBlock += [temp1]

        tempR = str.upper(random)
        j=len(inData)//16
        for k in range(0,j-1):
            sTempRes = str.upper(self.SSC_Xor(sBlock[k], tempR))
            tempR = self.DES_Cipher_CBC(sTempRes, DES3Key[:16])
        sTempRes = str.upper(self.SSC_Xor(sBlock[j-1], tempR))
        tempR = self.DES3_Cipher_CBC(sTempRes, DES3Key)
        return tempR[:2*8] 

    def MAC_SingleDESPlusTriDes_EnICV_8Bytes(self, random, inData, DES3Key):
        """
        This is also known as the Retail MAC. It is as defined in [ISO 9797-1] as MAC Algorithm 3 with output
        transformation 3, without truncation, and with DES taking the place of the block cipher.
        """
        random = str.upper(random)
        inData = str.upper(inData)
        DES3Key = str.upper(DES3Key)
        ICV = self.DES_Cipher_CBC(random, DES3Key[:16])
        random = ICV
        if len(inData)%16 == 0: 
            inData = inData+('8000000000000000')
        else:
            i = len(inData)%16
            k = 16-i
            inData = inData+'80'
            for j in range(1,k//2):
                inData = inData+'00'
        sBlock = []
        for i in range(1,(len(inData)//16)+1):
            k = 16*(i-1)+1
            temp1 = inData[k-1:k+15]
            sBlock += [temp1]

        tempR = str.upper(random)
        j=len(inData)//16
        for k in range(0,j-1):
            sTempRes = str.upper(self.SSC_Xor(sBlock[k], tempR))
            tempR = self.DES_Cipher_CBC(sTempRes, DES3Key[:16])
        sTempRes = str.upper(self.SSC_Xor(sBlock[j-1], tempR))
        tempR = self.DES3_Cipher_CBC(sTempRes, DES3Key)
        return tempR[:2*8]        
        
    def MAC_SingleDESPlusTriDes_4Bytes(self, random, inData, DES3Key):
        inData=str.upper(inData)
        if len(inData)%16 == 0: 
            inData = inData+('8000000000000000')
        else:
            i = len(inData)%16
            k = 16-i
            inData = inData+'80'
            for j in range(1,k//2):
                inData = inData+'00'
        
        sBlock = []
        for i in range(1,len(inData)//16+1):
            k = 16*(i-1)+1
            temp1 = inData[k-1:k+15]
            sBlock += [temp1]

        tempR = str.upper(random)
        j=len(inData)//16
        for k in range(0,j):
            sTempRes = str.upper(self.SSC_Xor(sBlock[k], tempR))
            tempR = str.upper(self.DES_Cipher_CBC(sTempRes, DES3Key[:16]))
            
        temp1 = self.DES_Decipher_CBC(tempR, DES3Key[16:32])
        tempRes = self.DES_Cipher_CBC(temp1, DES3Key[:16])

        return tempRes[:8]
        
    def MAC_DES3_Full(self, random, inData, DES3Key):
        """
        The full triple DES MAC is as defined in [ISO 9797-1] as MAC Algorithm 3 with output transformation 3, without
        truncation, and with triple DES taking the place of the block cipher.
        """
        
        inData=str.upper(inData)
        if len(inData)%16 == 0: 
            inData = inData+('8000000000000000')
        else:
            i = len(inData)%16
            k = 16-i
            inData = inData+'80'
            for j in range(1,k//2):
                inData = inData+'00'
        
        sBlock = []
        for i in range(1,len(inData)//16+1):
            k = 16*(i-1)+1
            temp1 = inData[k-1:k+15]
            sBlock += [temp1]

        tempR = str.upper(random)
        j=len(inData)//16
        for k in range(0,j):
            sTempRes = str.upper(self.SSC_Xor(sBlock[k], tempR))
            tempR = str.upper(self.DES3_Cipher_CBC(sTempRes, DES3Key))
            
        #temp1 = self.DES_Decipher(tempR, DES3Key[16:32])
        #tempRes = self.DES_Cipher(temp1, DES3Key[:16])

        #return tempRes
        return tempR
