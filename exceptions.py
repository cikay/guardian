class CustomException(Exception):
    """Custom base class for all exceptions in this module."""
    def __init__(self, messages: list[str], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.messages = messages