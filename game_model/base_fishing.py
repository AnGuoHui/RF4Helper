from abc import ABC, abstractmethod

class BaseFishing(ABC):
    
    @abstractmethod
    def fishing(self):
        pass