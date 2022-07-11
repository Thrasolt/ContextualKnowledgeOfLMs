from typing import List

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"

KEYS: List[str] = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

VALID_KEY_COMBS = [(SIMPLE, COMPOUND), (SIMPLE, COMPLEX), (SIMPLE, COMCOM),
                   (COMPOUND, COMPLEX), (COMPOUND, COMCOM), (COMPLEX, COMCOM)]

SUBJ_LABEL = "sub-label"
