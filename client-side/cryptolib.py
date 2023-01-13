from Crypto import Random
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from base64 import b64decode,b64encode, urlsafe_b64decode, urlsafe_b64encode
import hashlib
from Crypto.Cipher import PKCS1_OAEP

BS = 16
#pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
pad = lambda s: (s + ((BS - len(s) % BS) * chr(BS - len(s) % BS))).encode(encoding="utf-8")


unpad = lambda s : s[:-ord(s[len(s)-1:])]

def genRSAKey():	
	random_generator = Random.new().read
	key = RSA.generate(1024, random_generator)
	binPrivKey = key.exportKey('DER')
	binPubKey =  key.publickey().exportKey('DER')
	return b64encode(binPrivKey), b64encode(binPubKey)

def encAES(key, msg):
	key = hashlib.sha256(key.encode('utf-8')).hexdigest()[:BS]
	raw = pad(bytes(msg))
	#raw = pad(bytes(msg, encoding='utf8'))
	iv = Random.new().read(AES.block_size)
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return b64encode(iv + cipher.encrypt(raw)) 

def decAES(key, hdn_msg):
	key = hashlib.sha256(key.encode('utf-8')).hexdigest()[:BS]
	enc = b64decode(hdn_msg.encode('utf-8'))
	iv = enc[:BS]
	cipher = AES.new(key, AES.MODE_CBC, iv)
	return unpad(cipher.decrypt(enc[BS:]))

def encRSA(pubkey, msg):
	pubKeyObj =  RSA.importKey( b64decode( pubkey ) )
	hdn_msg = pubKeyObj.encrypt(msg, 'x')[0]
	return b64encode(hdn_msg)
	
def decRSA(privkey, hdn_msg):
	privKeyObj = RSA.importKey( b64decode( privkey ) )
	msg = privKeyObj.decrypt( b64decode(hdn_msg) )
	return msg

def GenRSA_1():
	key = RSA.generate(1024)
	private_key = key.export_key('PEM')
	public_key = key.publickey().exportKey('PEM')
	#print(private_key, public_key)
	return private_key.decode("ascii"), public_key.decode("ascii")
	
def GenRSA():
	key = RSA.generate(1024)
	private_key = key.export_key('PEM')
	public_key = key.publickey().exportKey('PEM')
	#print(private_key, public_key)
	return private_key.hex(), public_key.hex()

def encryptRSA_1(pk, message):
	message = str.encode(message)
	rsa_public_key = RSA.importKey(pk.encode('ascii'))
	rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
	encrypted_text = rsa_public_key.encrypt(message)
	return urlsafe_b64encode(encrypted_text).decode('ascii')

def encryptRSA(pk, message):
	message = str.encode(message)
	rsa_public_key = RSA.importKey(bytearray.fromhex(pk))
	rsa_public_key = PKCS1_OAEP.new(rsa_public_key)
	encrypted_text = rsa_public_key.encrypt(message)
	return urlsafe_b64encode(encrypted_text).decode('ascii')


def decryptRSA(pv, encdata ):
	encrypted_text = urlsafe_b64decode(encdata.encode('ascii'))
	rsa_private_key = RSA.importKey(bytearray.fromhex(pv))
	rsa_private_key = PKCS1_OAEP.new(rsa_private_key)
	decrypted_text = rsa_private_key.decrypt(encrypted_text)
	return decrypted_text.decode('ascii')


class AESCipher(object):
    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return urlsafe_b64encode(iv + cipher.encrypt(raw.encode())).decode('ascii')

    def decrypt(self, enc):
        enc = urlsafe_b64decode(enc.encode('ascii'))
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]
		
'''
keystr = "abcdefghijklmnopabcdefghijklmnop"
hello = "12345678901234567890123456789012345678901234567890"
print "Plain:",hello
enc1 = encAES(keystr,hello)
print enc1
dec1 = decAES(keystr,enc1)
print "Decrypted:",dec1
'''

if __name__ == "__main__":
	#print( genRSAKey() )
	
	mode = 1
	if mode == 0:
	
		aes = AESCipher("hello123")
		chiper = aes.encrypt("It is a hidden message")
		print(chiper)
		
		#print(chiper.decode('ascii'))
		#ascstr = chiper.decode('ascii')
		#byteval = ascstr.encode('ascii')
		aes2 = AESCipher("hello123")
		#plain = aes2.decrypt(byteval)
		plain = aes2.decrypt(chiper)
		print(plain)
	else:
		pv, pk = GenRSA()
		print(pv, pk)
		message = "hello there!"
		print(message)
		chiper = encryptRSA(pk, message)
		plain = decryptRSA(pv, chiper)
		print(chiper)
		print(plain)
		
