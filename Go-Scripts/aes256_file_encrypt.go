/* Author: Evangelos Dimoulis
 *
 * Implements AES256 GCM encryption/decryption using a random generated 32 byte key.
 * The file to encrypt is given as a command line argument.
 * Encrypted file is stored as 'ciphertext.bin'
 *
 * Execution example: go run aes256_file_encrypt.go test.txt
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
	"os"
	"fmt"
	"C"
	"time"
)

func main() {
	log.Println("File encryption example\n")
	
	// File as command line argument
	args := os.Args
	file_to_encrypt := args[1]

	// Generate a random 32 byte key for AES-256
	bytes := make([]byte, 32)
	if _, err := rand.Read(bytes); err != nil {
		panic(err.Error())
	}

	// Encode key in bytes to string and keep as secret, put in a vault
	keyString := hex.EncodeToString(bytes)
	fmt.Printf("Symmetric 32 Byte AES256 Key to encrypt/decrypt: %s\n", keyString)

	plaintext, err := ioutil.ReadFile(file_to_encrypt)
	if err != nil {
		log.Fatal(err)
	}

	encrypted := encrypt(plaintext, keyString)
	
	log.Println("\n")
	fmt.Printf("Encrypted data: %s\n", encrypted)
	
	decrypted := decrypt("ciphertext.bin", keyString)
	log.Println("\n")
	fmt.Printf("Decrypted file contents: %s\n", decrypted)

}
/* Encrypts a byte sequence when given a key strign encoded as an input
 * Return the encrypted file.
 */

func encrypt(stringToEncrypt []byte, keyString string) (encryptedString string){

	plaintext := stringToEncrypt
	
	// Since the key is in string, we need to convert decode it to bytes
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
	err = ioutil.WriteFile("ciphertext.bin", ciphertext, 0777)
	if err != nil {
		log.Panic(err)
	}

	return fmt.Sprintf("%x", ciphertext)
}


/* Decrypts an encrypted file using a keyString, saves the output to a file and returns a 
	a string contaning the contents
*/
func decrypt(encryptedFile string, keyString string) (decryptedString string){
	
	ciphertext, err := ioutil.ReadFile(encryptedFile)
	if err != nil {
		log.Fatal(err)	//duration := time.Since(start)
	//fmt.Println(duration)
	//time.Sleep(20*time.Second)

	}

	// Since the key is in string, we need to convert decode it to bytes
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

	err = ioutil.WriteFile("plaintext.txt", plaintext, 0777)
	if err != nil {
		log.Panic(err)
	}

	return fmt.Sprintf("%s", plaintext)
}