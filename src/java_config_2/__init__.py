import os

version = '@VERSION@' if not '@VERSION@'.startswith('@') else 'unknown'

eprefix_fallback = '@EPREFIX@' if not '@EPREFIX@'.startswith('@') else ''
eprefix = os.getenv('EPREFIX', eprefix_fallback)
