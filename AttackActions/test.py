import time
from processManagement.ProcessManager import ProcessManager
if __name__ == "__main__":
    pm = ProcessManager()

    # Define the command to run
    pm.define_command("ping -c 50 google.com")  # Change to any command you want to test

    # Start the process in a new thread
    pm.start_process()

    # Let the command run for a specific time
    time.sleep(10)  # Adjust the time based on your command

    # Kill the process and the terminal
    pm.kill_process()
