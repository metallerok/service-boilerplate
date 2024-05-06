from typing import Optional


class AttributeValidationError(AttributeError):
    def __init__(self, message: Optional[str] = None, *args):
        self.message = message

        super().__init__(*args)
