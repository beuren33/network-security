import sys
from Network_security.logging.logger import logging

class NetworkSecurityException(Exception):
    def __init__(self, error_message, error_details: sys):
        self.error_message = error_message
        _, _, exc_tb = error_details.exc_info()

        self.lineno = exc_tb.tb_lineno
        self.filename = exc_tb.tb_frame.f_code.co_filename
    
    def __str__(self):
        return "Erro ocorrido no script python [{0}] linha [{1}] mensagem de erro [{2}]".format(
            self.filename, self.lineno, str(self.error_message)
        )
    

