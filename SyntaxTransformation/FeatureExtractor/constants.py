from typing import List

SIMPLE = 'simple'
COMPOUND = 'compound'
COMPLEX = 'complex'
COMCOM = "compound-complex"
KEYS: List[str] = [SIMPLE, COMPOUND, COMPLEX, COMCOM]

ONE_TO_ONE = "1:1"
N_TO_ONE = "N:1"
N_TO_M = "N:M"
CARDINALITIES = [ONE_TO_ONE, N_TO_ONE, N_TO_M]

MASK = "[MASK]"
INPUT_ID_KEY = "input_ids"

