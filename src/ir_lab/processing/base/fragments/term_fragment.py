from .fragment import Fragment
from ir_lab.models.tokens import Token


class TermFragment(Fragment) : 
    content  : list[str | Token]
