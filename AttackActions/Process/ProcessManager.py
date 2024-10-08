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
            # Start the process without using a terminal emulator
            self.process = subprocess.Popen(
                self.command,
                shell=True,  # Execute command through the shell
                preexec_fn=os.setsid
            )
            self.process.wait()

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
        Kills the process and ensures proper cleanup of the thread.
        """
        if self.process:
            # Check if the process is still running
            if self.process.poll() is None:  # poll() returns None if process is still running
                try:
                    # Terminate the process and its process group
                    os.killpg(os.getpgid(self.process.pid), signal.SIGTERM)  # Kill process group
                    print("Process killed.")
                except OSError as e:
                    print(f"Error killing process: {e}")
            else:
                print("Process already terminated.")

            # Ensure the thread is properly cleaned up
            if self.thread.is_alive():
                self.thread.join()  # Wait for the thread to finish

        else:
            print("No process to kill.")

    def is_alive(self):
        return self.thread.is_alive()
