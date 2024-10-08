from Process.ProcessManager import ProcessManager
from ThreadManagement.ThreadDto import ThreadDto
from typing import List


class ThreadManager(object):

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ThreadManager, cls).__new__(cls)
            cls.threads: List[ThreadDto] = []
        return cls.instance

    # returns true if there is an error
    def check_for_error(self, attack: str) -> bool:
        print("Checking for errors")
        for thread in self.threads:
            if thread.get_attack() == attack:
                print("Checking for errors: attack found")
                try:
                    if thread.is_alive():
                        print("Checking for errors: Thread is alive")
                        return False
                except:
                    print("Checking for errors: Thread is dead")
                    self._remove_thread(threadDto=thread)
                    return True
        return False

    def _remove_thread(self, threadDto: ThreadDto):
        print("Removing Thread: Killing process")
        threadDto.get_thread().kill_process()
        print("Removing Thread: removing process")
        self.threads.remove(threadDto)

    # Adds thread and starts it

    def _add_thread(self, threadDto: ThreadDto):
        self.threads.append(threadDto)
        threadDto.get_thread().start_process()

    def stop_attack(self, attack: str) -> bool:
        print("Stopping the attack")
        if not self.check_for_error(attack=attack):
            print("Stopping the attack: there were no errors")
            for thread in self.threads:
                if thread.get_attack() == attack:
                    print("Stopping the attack: attack found!")
                    self._remove_thread(thread)
                    return True
        return False

    def start_attack(self, attack: str, command: str):
        processManager: ProcessManager = ProcessManager(command=command)
        threadDto: ThreadDto = ThreadDto(attack=attack, thread=processManager)
        self._add_thread(threadDto=threadDto)

    # Check if attack is running
    def check_running(self, attack: str) -> bool:
        for thread in self.threads:
            if thread.get_attack() == attack:
                return True
        return False
