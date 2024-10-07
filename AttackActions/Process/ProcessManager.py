from IProcessManager import IProcessManager
import threading
import subprocess
import os
import signal


class ProcessManager(IProcessManager):
    def __init__(self):
        self.command = None
        self.process = None
        self.thread = None

    def define_command(self, command: str):
        """
        Defines the command to be executed.
        """
        self.command = command

    def _run_command(self):
        """
        Internal function to run the command in a separate process.
        """
        if self.command:
            # Start the process without using a terminal emulator
            self.process = subprocess.Popen(
                self.command,
                shell=True,  # Execute command through the shell
                preexec_fn=os.setsid
            )
            self.process.wait()  # Wait for the command to complete

    def start_process(self):
        """
        Starts the process in a separate thread.
        """
        if self.command:
            # Create a thread to run the command
            self.thread = threading.Thread(target=self._run_command)
            self.thread.start()
        else:
            print("Command not defined. Use define_command() first.")

    def kill_process(self):
        """
        Kills the process.
        """
        if self.process:
            # Terminate the process
            os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)  # Kill process group
            self.thread.join()  # Wait for the thread to finish
            print("Process killed.")
        else:
            print("No process to kill.")