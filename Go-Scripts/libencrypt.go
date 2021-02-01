/* Author: Evangelos Dimoulis
 *
 * Implements AES256 GCM encryption/decryption using a 32 byte symmetric key.
 * The file to encrypt is given as a command line argument.
 * Encrypted file is stored as with the original filename and ends with '.bin' extension
 *
 * Execution example: go run libencrypt.go Input/test.txt Keys/key.dat
 * Export as C library: go build -buildmode=c-shared -o libencrypt.so libencrypt.go
 */

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
	"os"
	"strings"
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

	err = ioutil.WriteFile("original_file", plaintext, 0777)
	if err != nil {
		log.Panic(err)
	}
}


func main(){
	
	// File as command line argument
	args := os.Args
	file_path := args[1]
	key_path := args[2]

	tokens := strings.Split(file_path, "/")
	file_name := strings.Split(tokens[len(tokens) - 1], ".")[0]
	ciphertext := file_name + ".bin"

	encrypt(file_path, file_name, key_path)
	decrypt(ciphertext, key_path)
	
}
