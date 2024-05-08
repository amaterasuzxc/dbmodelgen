import pymorphy3
from typing import List


class ShapeShifter:
    def __init__(self) -> None:
        self._morph = pymorphy3.MorphAnalyzer()


    @staticmethod
    def _split(span: str) -> List[List[str]]:
        split = span.split(' ')
        split = list(map(lambda _:_.split('-'), split))

        return split


    @staticmethod
    def _is_noun(gramm: tuple) -> bool:
        return {'NOUN'} in gramm.tag


    @staticmethod
    def _is_adjective(gramm: tuple) -> bool:
        return gramm.tag.POS in {'ADJS', 'ADJF'}


    @staticmethod
    def _is_util(gramm: tuple) -> bool:
        return gramm.tag.POS in {'CONJ', 'PRCL', 'INTJ', 'PREP'}
    

    @staticmethod
    def _is_unknown(gramm: tuple) -> bool:
        return 'UNKN' in gramm.tag
    

    @staticmethod
    def _is_gold(gramm: tuple) -> bool:
        return (
            ShapeShifter._is_noun(gramm)
            or ShapeShifter._is_adjective(gramm)
            or ShapeShifter._is_util(gramm)
        )
    

    def _parse(self, word: str) -> tuple:
        parsed = self._morph.parse(word)
        if self._is_unknown(parsed[0]):
            return parsed[0]
        gold = list(filter(lambda _:self._is_gold(_), parsed))
        if not gold:
            return parsed[0]
        return max(gold, key=lambda g:g.score)
    

    def _normalize_gramm(self, gramm: tuple, single: bool = False) -> tuple:
        gramm = gramm.normalized
        if not self._is_gold(gramm) or self._is_util(gramm):
            pass
        elif 'Sgtm' in gramm.tag or single and 'Pltm' not in gramm.tag:
            gramm = gramm.inflect({'sing'})
        else:
            gramm = gramm.inflect({'plur', 'nomn'})
        return gramm
    

    def _process_gramm_pairs(self, gramms_list: List[tuple], i: int):
        size = len(gramms_list)
        result_list = []
        gramm = gramms_list[i]

        if (self._is_gold(gramm)):
            if i != 0 and self._is_noun(gramm) and self._is_noun(gramms_list[i-1]):
                result_list.append(gramm.inflect({gramm.tag.number, 'gent'}))
            elif i < size - 1 and self._is_adjective(gramm) and self._is_noun(gramms_list[i+1]):
                result_list.append(gramm.inflect({gramms_list[i+1].tag.number, 'nomn'}))
            elif i != 0 and self._is_adjective(gramm) and self._is_adjective(gramms_list[i-1]):
                result_list.append(gramm.inflect({gramms_list[i-1].tag.number, gramms_list[i-1].tag.gender}))
            elif self._is_util(gramm):
                result_list.append(gramm)
            elif self._is_noun(gramm):
                result_list.append(gramm.inflect({gramm.tag.number, 'nomn'}))
            else:
                result_list.append(gramm)
        else:
            result_list.append(gramm)
        
        i += 1

        if i < size:
            result_list += self._process_gramm_pairs(gramms_list, i)

        return result_list


    def _normalize(self, span: str, single: bool = False) -> str:
        split = self._split(span)

        phrases = []
        p_list = len(split) > 1

        for i in range(0, len(split)):
            phrase = split[i]
            words = []
            w_list = len(phrase) > 1

            if w_list:
                gramms_to_process = list(map(lambda _:self._normalize_gramm(self._parse(_), single), phrase))
                processed_gramms = self._process_gramm_pairs(gramms_to_process, 0)
                words += processed_gramms
            else:
                gramm = self._parse(phrase[0])
                gramm = self._normalize_gramm(gramm, single)
                words.append(gramm)

            phrases += words

        if p_list:
            gramms_to_process = phrases
            processed_gramms = self._process_gramm_pairs(gramms_to_process, 0)
            phrases = processed_gramms

        phrases = list(map(lambda _:_.word, phrases))

        return ' '.join(phrases)


    def shapeshift(self, span: str, single = False) -> str:
        return self._normalize(span, single)