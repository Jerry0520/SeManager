# -*- coding:utf-8 -*-
from .swapApdu import LV
from .Encryption import Encryption
from support.utils.contants import dict_isd_key

encryption = Encryption()

class gp():
        
        def __init__(self, CLA = '84'):
                self.CLA = CLA

        def deleteCommand(self,P1,P2,AID,random,DES3key):
                #P1: b8 = 0 Last (or only) command , b8 = 1 More DELETE commands
                #P2: b8 = 0 Delete object , b8 = 1 Delete object and related object
                CLA = self.CLA
                if CLA == '80':

                        APDU = '80E4' + P1 + P2 + LV(AID + '0000')+'4F'+ LV(AID) + AID                        
                elif CLA == '84':
                        APDU = '84E4' + P1 + P2 + LV(AID + '00000000000000000000') +'4F'+ LV(AID) + AID   
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC
 
                return APDU                
                 
        def getdataCommand(self,P1,P2,DATA,random,DES3key):
                #P1: '00' or high order tag value
                #P2: Low order tag value
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80CA' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84CA' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC
                
                return APDU
                        
        def getstatusCommand(self,P1,P2,DATA,random,DES3key):
                #P1: '80' Issuer Security Domain '40' Applications, including Security Domain
                #    '20' Executable Load Files only '10' Executable Load Files and their Executable Modules only
                #P2: b1 = 0 Get first or all occurrence(s) b1 = 1 Get next occurrence(s)
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80F2' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84F2' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC

                return APDU
        
        def installCommand(self,P1,P2,DATA,random,DES3key):
                '''
                P1:
                0  -  -  -  -  -  -  -  Last (or only) command
                1  -  -  -  -  -  -  -  More INSTALL commands
                -  1  0  0  0  0  0  0  For registry update
                -  0  1  0  0  0  0  0  For personalization
                -  0  0  1  0  0  0  0  For extradition
                -  0  0  0  1  -  -  0  For make selectable
                -  0  0  0  -  1  -  0  For install
                -  0  0  0  -  -  1  0  For load
                P2:
                ‘00’ indicates that no information is provided.
                ‘01’ indicates the beginning of the combined Load, Install and Make Selectable process.
                ‘03’ indicates the end of the combined Load, Install and Make Selectable process.
                '''
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80E6' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84E6' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC

                return APDU
                
        def loadCommand(self,P1,P2,DATA,random,DES3key):
                '''
                P1:
                0  -  -  -  -  -  -  -  More blocks
                1  -  -  -  -  -  -  -  Last block
                -  X  X  X  X  X  X  X  RFU
        
                P2:
                Reference control parameter P2 contains the block number, and shall be coded sequentially from '00' to 'FF'
                '''
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80E8' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84E8' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC

                return APDU


        def putkeyCommand(self,P1,P2,DATA,random,DES3key):
                '''
                P1:
                0  -  -  -  -  -  -  -  Last (or only) command
                1  -  -  -  -  -  -  -  More PUT KEY commands
                -  X  X  X  X  X  X  X  Key Version Number
         
                P2:
                0  -  -  -  -  -  -  -  Single key
                1  -  -  -  -  -  -  -  Multiple keys
                -  X  X  X  X  X  X  X  Key Identifier
                '''
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80D8' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84D8' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC

                return APDU
                        
                        
        def selectCommand(self,AID):
                APDU = '00A40400' +LV(AID) +AID

                return APDU
                
        def setstatusCommand(self,P1,P2,DATA,random,DES3key):
                '''
                P1:
                1  0  0  -  -  -  -  -  Indicate Issuer Security Domain
                0  1  0  -  -  -  -  -  Indicate Application or Supplementary Security Domain
                0  1  1  -  -  -  -  -  Indicate Security Domain and its associated Applications
                -  -  -  X  X  X  X  X  RFU
         
                P2:
                b8 = 1 indicates a transition to the LOCKED state;
                b8 = 0 indicates a transition (from LOCKED) back to the previous state
                '''
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80F0' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84F0' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC

                return APDU
                        
        def storedataCommand(self,P1,P2,DATA,random,DES3key):
                '''
                P1:
                0  -  -  -  -  -  -  -  More blocks
                1  -  -  -  -  -  -  -  Last block
                -  0  0  -  -  -  -  -  No general encryption information or non-
                encrypted data
                -  0  1  -  -  -  -  -  Application dependent encryption of the data
                -  1  0  -  -  -  -  -  RFU (encryption indicator)
                -  1  1  -  -  -  -  -  Encrypted data
                -  -  -  0  0  -  -  -  No general data structure information
                -  -  -  0  1  -  -  -  DGI format of the command data field
                -  -  -  1  0  -  -  -  BER-TLV format of the command data field
                -  -  -  1  1  -  -  -  RFU (data structure information)
                -  -  -  -  -  X  X  X  RFU
         
                P2:
                Reference control parameter P2 shall contain the block number coded sequentially from '00' to 'FF'. The
        Security Domain shall check the sequence of commands
                '''
                
                CLA = self.CLA
                if CLA =='80':
                        APDU = '80E2' + P1 + P2 + LV(DATA) + DATA
                elif CLA == '84':
                        APDU = '84E2' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                        MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                        APDU += MAC

                return APDU
        
        def initializeupdateCommand(self,P1,P2,DATA):
                '''
                P1:Key Version Number  
                P2:Key Identifier
                '''
                
                APDU = '8050' + P1 + P2 + LV(DATA) + DATA

                return APDU  
        
        def externalauthenticateCommad(self,P1,P2,DATA,random,DES3key):
                '''
                P1:Security level
                0  0  0  0  0  0  1  1  C-DECRYPTION and C-MAC.
                0  0  0  0  0  0  0  1  C-MAC
                0  0  0  0  0  0  0  0  No secure messaging expected
                P2:The reference control parameter P2 shall always be set to '00'
                '''
                
                APDU = '8482' + P1 + P2 + LV(DATA + '0000000000000000') + DATA
                MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, APDU, DES3key)
                APDU += MAC

                return APDU  
        
        def gpexternalauthenticate(self,response,KENC,KMAC,KDEK):

                keyDiversificationData = response[4:20]
                keyInformation = response[24:28]
                cardChallenge = response[28:40]
                cardCryptogram = response[40:56]


                temp = '0182' + keyInformation + '000000000000000000000000'
                S_ENC = encryption.DES3_Cipher_CBC(temp, KENC)
                temp = '0181' + keyInformation + '000000000000000000000000'
                S_DEK = encryption.DES3_Cipher_CBC(temp, KDEK)
                
                SMACtemp = encryption.DES3_Cipher_ECB(keyInformation + cardChallenge, S_ENC)
                SMACtemp = encryption.SSC_Xor(SMACtemp, '1122334455667788')
                SMACtemp = encryption.DES3_Cipher_ECB(SMACtemp, S_ENC)
                SMACtemp = encryption.SSC_Xor(SMACtemp, '8000000000000000')
                hostCryptogram = encryption.DES3_Cipher_ECB(SMACtemp, S_ENC)
                
                temp = '0101' + keyInformation +'000000000000000000000000'
                S_MAC = encryption.DES3_Cipher_CBC(temp, KMAC)
                
                #response,sw1,sw2,mac = self.externalauthenticateCommad('84',securLevel,'00',hostCryptogram,'0000000000000000',S_MAC)
                
                return hostCryptogram, S_ENC, S_DEK, S_MAC
                
        def initkey(self,cplc):
                R_KENC = encryption.DES3_Cipher_ECB(cplc, dict_isd_key["KENC"])
                R_KMAC = encryption.DES3_Cipher_ECB(cplc, dict_isd_key["KMAC"])
                R_KDEK = encryption.DES3_Cipher_ECB(cplc, dict_isd_key["KDEK"])
                return R_KENC, R_KMAC, R_KDEK
        
        def sessionkey(self, random, key):
                sessionkey = encryption.DES_Cipher_CBC(random, key)
                return sessionkey
        
        def apdumac(self,random, data, sessionkey):
                MAC = encryption.MAC_SingleDESPlusTriDes_8Bytes(random, data, sessionkey)
                APDU = data + MAC
                return APDU

if __name__ == '__main__':
        gp = gp()
        KENC, KMAC, KDEK = gp.initkey('12345678123456781234567812345678')
        hostCryptogram, S_ENC, S_DEK, S_MAC = gp.gpexternalauthenticate('0000000000000000000020020005765C6F76257B31C479DAF06699B7', KENC, KMAC, KDEK)
        eaAPDU = gp.externalauthenticateCommad(P1='01', P2='00', DATA=hostCryptogram, random='0000000000000000', DES3key=S_MAC)
        #response,sw1,sw2,mac = gp.gpexternalauthenticate('D1560001010001600000000100000000','01','00','E4019B61187698B7F859558ADEC39DDD','E4019B61187698B7DD346BE2996661A6','E4019B61187698B756000BFA30E20762')
        #response,sw1,sw2 = gp.installCommand('84', '80', '00', '1122334455667788', 'D87B11926004FAA9', 'cf79017f86fe59d6de677cf1ea97dca1')
        #response,sw1,sw2 = deleteCommand(connection, '84', '80', '00', '1122334455667788', 'D87B11926004FAA9', 'cf79017f86fe59d6de677cf1ea97dca1') 
        #response,sw1,sw2 = gp.deleteCommandFree('80', '00', '1122334455667788')
        #print response,sw1,sw2
        #response,sw1,sw2,mac = gp.deleteCommand(CLA, P1, P2, DATA, random, DES3key)
        #print response,sw1,sw2,mac
        
        
        