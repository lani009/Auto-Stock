from abc import ABCMeta, abstractmethod


class Condition(metaclass=ABCMeta):
    def __init__():
        pass

    @abstractmethod
    def condition(self, parameter_list):
        """
        docstring
        """
        raise NotImplementedError

    def get_requirements():
        pass
