# Password Manager
This is a password manager that can store all our credentials. The credentials are encrypted using a master password with PBKDF2 hashing.
# Functioning
For first time users, there is a provision to create a master password in order to store all the credentials. It stores the username/email and password. 
For users who have created a master password can view the existing password and also add new password by choosing the appropriate option from the menu. The password stored can be a custom password or a randomly generated one with user given length. The credentials.txt holds the credentials and only upon entering the master password it is decrypted and viewable.
# Requirements and Installations
Clone this repository and run pip install -r installations.txt
Open the terminal and enter python3 password_manager.py
