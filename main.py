from typing import Optional, Tuple

class Token :
    def __init__(self, token_type: str, token_pos: Tuple[int,int], token_value : Optional[int] = None, token_string : Optional[str] = None):
        self.token_type = token_type
        self.token_pos = token_pos
        self.token_value = token_value
        self.token_string = token_string

