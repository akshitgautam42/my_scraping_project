class BaseStorage:
    """
    Abstract base class for storage handling.
    All storage classes should inherit from this class and implement its methods.
    """

    def save(self, data):
        """
        Save data to the storage.
        This method needs to be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")

    def load(self):
        """
        Load data from the storage.
        This method needs to be overridden by subclasses.
        """
        raise NotImplementedError("Subclasses must implement this method")
