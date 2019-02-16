#!/usr/bin/env python
#
# Python version 2.7.5
# Very simple Python script to dump all emails in an IMAP mailbox.
# Some security settings might be needed for the specific email service provider.
# iCloud needs an app-specific password: https://support.apple.com/en-ie/HT204397
# GMail needs to enable: "allowing access to less secure apps"
#

import sys
import imaplib
import os
import sys
import email
import getpass

#iCloud
IMAP_SERVER = 'imap.mail.me.com'
PORT = 993
EMAIL_ACCOUNT = "your_username@icloud.com"
USING_SSL = True
PASSWORD = 'your_password'

#GMAIL
#IMAP_SERVER = 'imap.gmail.com'
#PORT = 993
#EMAIL_ACCOUNT = "your_username"
#USING_SSL = True
#PASSWORD = getpass.getpass()

#LOCAL
#IMAP_SERVER = '127.0.0.1'
#PORT = 143
#EMAIL_ACCOUNT = "test"
#USING_SSL = False
#PASSWORD = getpass.getpass()

# application settings
MESSAGE_DIRECTORY = "./mail_backup"
MESSAGE_LOG_ERR_PATH = MESSAGE_DIRECTORY + "/" + "log_err.txt"
MESSAGE_LOG_INFO_PATH = MESSAGE_DIRECTORY + "/" + "log_info.txt"

if not os.path.exists(MESSAGE_DIRECTORY):
    os.makedirs(MESSAGE_DIRECTORY)
log_err_file = open (MESSAGE_LOG_ERR_PATH,'wb')
log_info_file = open (MESSAGE_LOG_INFO_PATH,'wb')

def log_err(message):
    log_err_file.write(message + "\n")
    print message
    
def log_info(message):
    log_info_file.write(message + "\n")    
    print message
    
def getSize(filename):
    st = os.stat(filename)
    return st.st_size

def main():

	#connect to the server
    if USING_SSL == False:
        M = imaplib.IMAP4(IMAP_SERVER,PORT)
    else:
        M = imaplib.IMAP4_SSL(IMAP_SERVER,PORT)
    M.login(EMAIL_ACCOUNT, PASSWORD)
	
	# get folder list
    rv,mailboxes = M.list("","*")

    log_info("listing mailboxes:" + str(mailboxes))

    if rv == 'OK':
        foldername = ""
        count =0
        for folder in  mailboxes:
            #print folder
            try:
                folder_parts = folder.split(' "/" ')
                foldername = folder_parts[1]
            except:
                log_info(folder)
                log_err("Error processing folder: " + folder)
                continue
            if not foldername:
                continue
            try:
				# process every single folder
                rv, data = M.select(foldername)
                MESSAGE_DIRECTORY_NAME = MESSAGE_DIRECTORY + "/" + foldername.replace("\"", "")
                if not os.path.exists(MESSAGE_DIRECTORY_NAME):
                    os.makedirs(MESSAGE_DIRECTORY_NAME)
                else:
                    log_info("Skipping already downloaded folder: " + foldername)
                    continue
            except:
                log_err("Error selecting folder: " + foldername)
                continue
            if rv == 'OK':
                log_info("Processing folder: " + foldername)
                #process_mailbox(M)
                rv, data = M.search(None, "ALL")
            if rv != 'OK':
                log_err("No messages found for folder: " + foldername)
            counter = 0
			# save all the messages
            for num in data[0].split():
                try:
                    rv, data = M.fetch(num, '(RFC822)')
                    if rv != 'OK':
                        log_err("ERROR getting message: " + num)
                        continue
                except:
                    log_err("Error fetching message: " + num + " for folder: " + foldername)
                    continue
                msgfile = MESSAGE_DIRECTORY_NAME + "/" + str(num) + ".eml"
                log_info("Writing message " + msgfile)
                f = open(msgfile.strip() , 'wb')
                try:
                    f.write(data[0][1])
                except:
                    f.close()
                    log_err("Error processing: " + msgfile)
                    continue
                f.close()
                counter = counter + 1
                #limit number of messages retrieved
                #if counter == 2:
                #   break
    else:
        log_err("ERROR: Unable to list folders ")
    if rv == 'OK':
        M.close()

    M.logout()

    #cleanup
    log_err_file.close()
    log_info_file.close()

if __name__ == "__main__":
    main()

