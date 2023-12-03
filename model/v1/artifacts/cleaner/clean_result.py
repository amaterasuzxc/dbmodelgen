import pymorphy3


morph = pymorphy3.MorphAnalyzer()

trash_list = ['"', '.', ',', '!', '?', '\'', ';', ':', '\n']


def defaultize(lst, trash_list):
    for trash in trash_list:
        lst = list(map(lambda _:_.replace(trash, ' '), lst))
    lst = list(map(lambda _:_.lower().strip(), lst))
    return lst


def group_split(lst):
    splitted = []
    for e in lst:
        split = e.split(' ')
        split = list(map(lambda _:_.split('-'), split))
        splitted.append(split)
    return splitted


def is_noun(gramm):
    return {'NOUN'} in gramm.tag


def is_adjective(gramm):
    return gramm.tag.POS in {'ADJS', 'ADJF', 'PRTF'}


def is_util(gramm):
    return gramm.tag.POS in {'CONJ', 'PRCL', 'INTJ', 'PREP'}


def process_gramm_pairs(gramms_list, i):
    size = len(gramms_list)
    result_list = []
    gramm = gramms_list[i]
    if i != 0 and is_noun(gramm) and is_noun(gramms_list[i-1]):
        result_list.append(gramm.inflect({gramm.tag.number, gramm.tag.case}))
    elif i < size - 1 and is_adjective(gramm):
        result_list.append(gramm.inflect({gramms_list[i+1].tag.number, 'nomn'}))
    elif is_util(gramm):
        result_list.append(gramm)
    else:
        result_list.append(gramm.inflect({gramm.tag.number, 'nomn'}))
    i += 1
    if i < size: result_list += process_gramm_pairs(gramms_list, i)
    return result_list


def normalize(lst):
    entries = []
    for entry in lst:
        phrases = []
        p_list = len(entry) > 1
        for i in range(0, len(entry)):
            phrase = entry[i]
            words = []
            w_list = len(phrase) > 1
            if w_list:
                gramms_to_process = list(map(lambda _:morph.parse(_)[0], phrase))
                processed_gramms = process_gramm_pairs(gramms_to_process, 0)
                words += processed_gramms
            else:
                gramm = morph.parse(phrase[0])[0]
                gramm = gramm.normalized
                if {'NOUN', 'plur'} in gramm.tag or {'NOUN'} in gramm.tag:
                    gramm = gramm.inflect({'plur', 'nomn'})
                words.append(gramm)
            phrases += words
        if p_list:
            gramms_to_process = phrases
            processed_gramms = process_gramm_pairs(gramms_to_process, 0)
            phrases = processed_gramms
        phrases = list(map(lambda _:_.word, phrases))
        entries.append(' '.join(phrases))
    return entries


def find_in_list(lst, substr):
    findings = []
    for e in lst:
        if substr in e:
            findings.append(e)
    return findings

def find_in_list_not_equals(lst, entry):
    for e in lst:
        if entry in e and entry != e: return e


def retain_distinct(lst): # TODO: change removal factor
    lst = list(set(lst))
    lst.sort()
    for e in lst:
        occurances = find_in_list(lst, e)
        cnt = len(occurances)
        if cnt == 2:
            to_remove = find_in_list_not_equals(occurances, e)
            lst.remove(to_remove)
        elif cnt > 2:
            lst.remove(e)
    return lst


def clean(lst):
    lst = defaultize(lst, trash_list)
    splitted = group_split(lst)
    normalized = normalize(splitted)
    distinct = retain_distinct(normalized)
    return distinct
