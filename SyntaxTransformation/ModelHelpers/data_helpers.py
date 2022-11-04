from typing import Tuple, Callable, List, Dict

MASK = "[MASK]"


def create_hard_filter_getter(
        model: Callable[[str], List[str]],
        templater: Callable[[str, str, str], Dict[str, str]]
        ) -> Callable[[str], Callable[[Tuple[str, str]], bool]]:

    def get_hard_filter(relation: str) -> Callable[[Tuple[str, str]], bool]:
        def hard_filter(subj_obj: Tuple[str, str]) -> bool:
            subj, obj = subj_obj
            unk_sentences: Dict[str, str] = templater(relation, "unk", MASK)
            for sentence in unk_sentences.values():
                if obj in model(sentence)[0:10]:
                    return False
            return True

        return hard_filter
    return get_hard_filter


def create_known_filter_getter(
        model: Callable[[str], List[str]],
        templater: Callable[[str, str, str], Dict[str, str]],
        cardinality: Callable[[str], str]
        ) -> Callable[[str], Callable[[Tuple[str, str]], bool]]:

    def get_known_filter(relation: str) -> Callable[[Tuple[str, str]], bool]:
        def known_filter(subj_obj: Tuple[str, str]) -> bool:
            subj, obj = subj_obj
            sentence: str = templater(relation, subj, MASK)["simple"]
            result: List[str] = model(sentence)
            if cardinality(relation) == "N:M":
                if obj in result[0:10]:
                    return True
                return False
            else:
                return obj == result[0]

        return known_filter
    return get_known_filter

