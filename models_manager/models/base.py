from abc import ABC, abstractmethod

class Model(ABC):
    """this class the methods that 
    should be implemented in each model instance"""

    is_running: bool

    @abstractmethod
    def run(self):
        pass
    @abstractmethod
    def stop(self):
        pass
