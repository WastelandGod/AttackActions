from Process.ProcessManager import ProcessManager


class ThreadDto:
    def __init__(self, attack: str, thread: ProcessManager):
        self.attack = attack
        self.thread = thread

    def get_attack(self) -> str:
        return self.attack

    def get_thread(self) -> ProcessManager:
        return self.thread
