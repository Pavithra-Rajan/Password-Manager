import string
import random
import os
from cryptography.fernet import Fernet, InvalidToken
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import base64
from cryptography.hazmat.backends import default_backend
strong_pass=string.ascii_letters + string.punctuation + string.digits  

def Credentials():
    website_name=input("Enter the website (just the root domain): ")
    user=input("Enter the username/email for the site: ")
    print("*"*20)
    print("Enter 1 to store randomly generated password")
    print("Enter 2 to store custom password")
    print("*"*20)
    option_pass=input()

    if option_pass == '1':
            length_pass =int(input("Enter the length of the new password: "))
            password="".join(random.sample(strong_pass,length_pass))
    elif option_pass == '2':
        password=input("Enter the password of your choice: ")
    
    return [website_name,user,password]

def master_fetch(opt_master):
    if opt_master == "new":
        master_send=input("Enter a master password to store all the credentials. Do not forget this!: ").encode()
    if opt_master == "exist":
        master_send=input("Enter your master password: ").encode()
    return master_send

def key_derivation(master,salt=None):
    if salt!=None:
        with open("salt_file.txt","wb") as st:
            st.write(salt)
    elif salt == None:
        try:
                with open("salt_file.txt","rb") as st:
                    salt=st.read()
        except FileNotFoundError:
            print("No password exist. it may either have been deleted or the credential file doesn't exist")
            quit()
    pbk_algo=PBKDF2HMAC(algorithm=hashes.SHA256(),length=32,salt=salt,iterations=100000,backend=default_backend())
    new_pass=base64.urlsafe_b64encode(pbk_algo.derive(master))
    return new_pass

def write_cred(website_name,user,password,method):
    str1='\n'+website_name+'\n'
    str2='User Name: '+user+'\n'
    str3='Decrypted Password: '+password+'\n'
    with open("credentials.txt",method) as fp:
        fp.write(str1+str2+str3)

def decrypt(new_pass):
    fernet=Fernet(new_pass)
    with open("credentials.txt") as fp:
        enc_data=fp.read()
        #print(enc_data)
    try:
            dec_data=fernet.decrypt(bytes(enc_data,encoding='utf8'))
            with open("credentials.txt","w") as file:
                file.write(dec_data.decode())
            file.close()
            print("FILE DECRYPTED")
            f=open("credentials.txt","r")
            file_print=f.read()
            print(file_print)

            return 1
    except InvalidToken:
        print("WRONG PASSWORD")
        return 0
       # quit()
def encrypt(new_pass,type):
    fernet=Fernet(new_pass)
    with open("credentials.txt") as fp:
        enc_data=fp.read()
    enc_data_encrypted=fernet.encrypt(bytes(enc_data,encoding='utf8'))
    with open("credentials.txt","w") as file:
                file.write(enc_data_encrypted.decode())
    if type==1:
        print("CREDENTIALS ENCRYPTED")
    if type==2:
        quit()
    if type==3:
        print("ENCRYPTED")
print("*"*80)
print("This is a Password Manager\n")
print("*"*80)
print("For first time users, type 'First' ")
print("For existent users, type 'Existing' ")
print("To exit, type 'Quit' ")
print("*"*80)
user_option=input("Enter First/Existing/Quit: ").lower()
while(user_option!="quit"):
        
    if user_option=='first':
        website_name,user,password=[str(i) for i in Credentials()]
        master=master_fetch("new")
        salt=os.urandom(16)
        key_enc=key_derivation(master,salt)

        write_cred(website_name,user,password,'w')
        encrypt(key_enc,1)
        
    if user_option=="existing":
        print("To enter new password press 1 ")
        print("To view new passwords press 2")
        op_exist=input("Enter your choice: ")
        if op_exist == '1':
            master=master_fetch("exist")
            key_enc=key_derivation(master)
            flag=decrypt(key_enc)
            if(flag==1):
                website_name,user,password=[str(i) for i in Credentials()]
                write_cred(website_name,user,password,'a')
                encrypt(key_enc,1)
        if op_exist=='2':
            master=master_fetch("exist")
            key_enc=key_derivation(master)
            flag=decrypt(key_enc)
            if(flag==1):
                encrypt(key_enc,3)
                #print("FILE ENCRYPTED")
    print("*"*80)
    print("\nFor first time users, type 'First' ")
    print("For existent users, type 'Existing' ")
    print("To exit, type 'Quit' ")
    print("*"*80)
    user_option=input("Enter First/Existing/Quit: ").lower()


