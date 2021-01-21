package main

import (
	"crypto/aes"
	"crypto/cipher"
	"crypto/rand"
	"encoding/hex"
	"io"
	"io/ioutil"
	"log"
	"C"
)

//export encrypt
func encrypt(fileToEncrypt string, fileName string, pathToKey string) *C.char{

	encrypted_file := fileName + ".bin"
	plaintext, err := ioutil.ReadFile(fileToEncrypt)
	if err != nil {
		log.Fatal(err)
	}

	// Read key file content and convert it to string
	content, err := ioutil.ReadFile(pathToKey)
	keyString := string(content)

	if err != nil {
		log.Fatal(err)
	}

	// Decode key in order to get the key as type byte[]
	key, _ := hex.DecodeString(keyString)

	block, err := aes.NewCipher(key)
	if err != nil {
		log.Panic(err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		log.Panic(err)
	}
	
	// Never use more than 2^32 random nonces with a given key
	// because of the risk of repeat.
	nonce := make([]byte, gcm.NonceSize())
	if _, err := io.ReadFull(rand.Reader, nonce); err != nil {
		log.Fatal(err)
	}

	ciphertext := gcm.Seal(nonce, nonce, plaintext, nil)
	
	// Save back to file
	err = ioutil.WriteFile(encrypted_file, ciphertext, 0777)
	if err != nil {
		log.Panic(err)
	}

	return C.CString(encrypted_file)

}

//export decrypt
func decrypt(fileToDecrypt string, pathToKey string){

	ciphertext, err := ioutil.ReadFile(fileToDecrypt)
	if err != nil {
		log.Fatal(err)
	}

	// Read key file content and convert it to string
	content, err := ioutil.ReadFile(pathToKey)
	keyString := string(content)

	if err != nil {
		log.Fatal(err)
	}

	// Decode key in order to get the key as type byte[]
	key, _ := hex.DecodeString(keyString)

	block, err := aes.NewCipher(key)
	if err != nil {
		log.Panic(err)
	}

	gcm, err := cipher.NewGCM(block)
	if err != nil {
		log.Panic(err)
	}

	nonce := ciphertext[:gcm.NonceSize()]
	ciphertext = ciphertext[gcm.NonceSize():]
	plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
	if err != nil {
		log.Panic(err)
	}

	err = ioutil.WriteFile("decrypted", plaintext, 0777)
	if err != nil {
		log.Panic(err)
	}
}


func main(){
	
	plaintext := "/home/edimoulis/Pictures/dd.png" //"/home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/test.txt"
	key_file := "/home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/key.dat"
	ciphertext := "/home/edimoulis/Master/Semester3/Security-of-Computer-Systems/Project/dd.bin"

	encrypt(plaintext, "test", key_file)
	decrypt(ciphertext , key_file)
	
}