import streamlit as st
from ThreadManagement.ThreadManager import ThreadManager
import time
attack = "Ping"
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
if st.button("Start attack"):
    command = "ping -c 50 google.com"
    threadManager.start_attack(attack=attack, command=command)
    output_placeholder = st.empty()
    while True:
        output = threadManager.check_for_output(attack)
        if output:
            output_placeholder.text(output)
        else:
            output_placeholder.text("No output yet...")
        time.sleep(1)  # Sleep to avoid excessive resource usage
