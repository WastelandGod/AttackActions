from abc import ABC, abstractmethod

class IProcessManager(ABC):
    @abstractmethod
    def kill_process(self):
        pass

    @abstractmethod
    def define_command(self, command : str):
        pass

    @abstractmethod
    def start_process(self):
        pass