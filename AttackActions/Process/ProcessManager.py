from Process.IProcessManager import IProcessManager
import threading
import subprocess
import os
import signal


class ProcessManager(IProcessManager):
    def __init__(self, command: str):
        self.command = command
        self.process = None
        self.thread = None
        self.thread_error = None  # To store any errors that occur during command execution

    def define_command(self, command: str):
        """
        Defines the command to be executed.
        """
        self.command = command

    def _run_command(self):
        """
        Internal function to run the command in a separate process and capture output and errors.
        """
        if self.command:
            try:
                # Start the process and capture stdout and stderr
                self.process = subprocess.Popen(
                    self.command,
                    shell=True,  # Execute command through the shell
                    stdout=subprocess.PIPE,  # Capture standard output
                    stderr=subprocess.PIPE,  # Capture standard error
                    preexec_fn=os.setsid,
                    text=True  # Ensure the output is in string format (not bytes)
                )

                # Capture the error streams
                stderr = self.process.communicate()

                self.thread_error = stderr

            except Exception as e:
                # Capture the exception and store it in thread_error
                self.thread_error = str(e)

    def start_process(self):
        """
        Starts the process in a separate thread and captures the output and errors.
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
