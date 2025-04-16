class GenericException(Exception):
    """Base class for all GAVA related exceptions"""

    def __init__(self, status_code, err_code, description):
        self.status_code = status_code
        self.err_code = err_code
        self.description = description
        super().__init__(self.err_code, self.description, self.status_code)