import logging

from pypinyin import pinyin, Style

initial_map = {
    'ㄅ': 'ㅂ', 'ㄆ': 'ㅍ', 'ㄇ': 'ㅁ', 'ㄈ': 'ㅍ',
    'ㄉ': 'ㄷ', 'ㄊ': 'ㅌ', 'ㄋ': 'ㄴ', 'ㄌ': 'ㄹ',
    'ㄍ': 'ㄱ', 'ㄎ': 'ㅋ', 'ㄏ': 'ㅎ',
    'ㄐ': 'ㅈ', 'ㄑ': 'ㅊ', 'ㄒ': 'ㅅ',
    'ㄓ': 'ㅈ', 'ㄔ': 'ㅊ', 'ㄕ': 'ㅅ', 'ㄖ': 'ㄹ',
    'ㄗ': 'ㅉ', 'ㄘ': 'ㅊ', 'ㄙ': 'ㅆ',
    '': '',
}

final_map = {
    'ㄚ': 'ㅏ', 'ㄛ': 'ㅗ', 'ㄜ': 'ㅓ', 'ㄝ': 'ㅔ', 'ㄧ': 'ㅣ', 'ㄨ': 'ㅜ', 'ㄩ': 'ㅟ',
    'ㄞ': 'ㅏ이', 'ㄟ': 'ㅔ이', 'ㄠ': 'ㅏ오', 'ㄡ': 'ㅓ우',
    'ㄢ': 'ㅏㄴ', 'ㄣ': 'ㅓㄴ', 'ㄤ': 'ㅏㅇ', 'ㄥ': 'ㅓㅇ', 'ㄦ': 'ㅓㄹ',
    'ㄧㄚ': 'ㅑ', 'ㄧㄛ': 'ㅛ', 'ㄧㄝ': 'ㅖ', 'ㄧㄞ': 'ㅑ이', 'ㄧㄠ': 'ㅑ오', 'ㄧㄡ': 'ㅠ', 'ㄧㄢ': 'ㅖㄴ', 'ㄧㄣ': 'ㅣㄴ', 'ㄧㄤ': 'ㅑㅇ', 'ㄧㄥ': 'ㅣㅇ',
    'ㄨㄚ': 'ㅘ', 'ㄨㄛ': 'ㅝ', 'ㄨㄞ': 'ㅙ', 'ㄨㄟ': 'ㅜ이', 'ㄨㄢ': 'ㅘㄴ', 'ㄨㄣ': 'ㅜㄴ', 'ㄨㄥ': 'ㅜㅇ',
    'ㄩㄝ': 'ㅞ',  'ㄩㄢ': 'ㅟ안', 'ㄩㄣ': 'ㅟㄴ', 'ㄩㄥ': 'ㅠㅇ',
}

final_map_alone = {
    'ㄨㄟ': 'ㅞ이', 'ㄨㄣ': 'ㅝㄴ', 'ㄨㄥ': 'ㅝㅇ',
}

onset_table = {
    '': 11, 'ㄱ': 0, 'ㄲ': 1, 'ㄴ': 2, 'ㄷ': 3, 'ㄸ': 4, 'ㄹ': 5, 'ㅁ': 6,
    'ㅂ': 7, 'ㅃ': 8, 'ㅅ': 9, 'ㅆ': 10, 'ㅇ': 11, 'ㅈ': 12, 'ㅉ': 13,
    'ㅊ': 14, 'ㅋ': 15, 'ㅌ': 16, 'ㅍ': 17, 'ㅎ': 18,
}

nucleus_table = {
    'ㅏ': 0, 'ㅐ': 1, 'ㅑ': 2, 'ㅒ': 3, 'ㅓ': 4, 'ㅔ': 5, 'ㅕ': 6, 'ㅖ': 7,
    'ㅗ': 8, 'ㅘ': 9, 'ㅙ': 10, 'ㅚ': 11, 'ㅛ': 12, 'ㅜ': 13, 'ㅝ': 14,
    'ㅞ': 15, 'ㅟ': 16, 'ㅠ': 17, 'ㅡ': 18, 'ㅢ': 19, 'ㅣ': 20,
}

coda_table = {
    '': 0, 'ㄱ': 1, 'ㄲ': 2, 'ㄳ': 3, 'ㄴ': 4, 'ㄵ': 5, 'ㄶ': 6,
    'ㄷ': 7, 'ㄹ': 8, 'ㄺ': 9, 'ㄻ': 10, 'ㄼ': 11, 'ㄽ': 12, 'ㄾ': 13,
    'ㄿ': 14, 'ㅀ': 15, 'ㅁ': 16, 'ㅂ': 17, 'ㅄ': 18, 'ㅅ': 19, 'ㅆ': 20,
    'ㅇ': 21, 'ㅈ': 22, 'ㅊ': 23, 'ㅋ': 24, 'ㅌ': 25, 'ㅍ': 26, 'ㅎ': 27,
}

def combine_hangul(onset, nucleus, coda=''):
    sp_onset = ['ㅈ', 'ㅉ', 'ㅊ']
    sp_nucleus = ['ㅑ', 'ㅖ', 'ㅛ', 'ㅠ']
    rule_nuclues = ['ㅏ', 'ㅔ', 'ㅗ', 'ㅜ']
    if onset in sp_onset and nucleus in sp_nucleus:
        nucleus = rule_nuclues[sp_nucleus.index(nucleus)]

    try:
        onset_index = onset_table[onset]
        nucleus_index = nucleus_table[nucleus]
        coda_index = coda_table.get(coda, 0)
        code = 0xAC00 + (onset_index * 21 * 28) + (nucleus_index * 28) + coda_index
        return chr(code)
    except:
        return onset + nucleus + coda

def is_hangul_syllable(char):
    code = ord(char)
    return 0xAC00 <= code <= 0xD7A3

def is_chinese_char(char):
    code = ord(char)
    return (
        0x4E00 <= code <= 0x9FFF or     # CJK Unified Ideographs
        0x3400 <= code <= 0x4DBF or     # CJK Unified Ideographs Extension A
        0x20000 <= code <= 0x2A6DF or   # Extension B
        0x2A700 <= code <= 0x2B73F or   # Extension C
        0x2B740 <= code <= 0x2B81F or   # Extension D
        0x2B820 <= code <= 0x2CEAF or   # Extension E
        0xF900 <= code <= 0xFAFF        # CJK Compatibility Ideographs
    )

def chinese_to_hangul(text):
    result = []

    for char in text:
        if not is_chinese_char(char):
            result.append(char)
            continue

        zhuyin = pinyin(char, style=Style.BOPOMOFO, strict=False)[0][0]

        onset = ''
        nucleus = ''
        coda = ''

        for sound in ['ˊ', 'ˇ', 'ˋ', '˙']:
            zhuyin = zhuyin.replace(sound, '')

        if zhuyin[0] in initial_map:
            onset = initial_map[zhuyin[0]]
            zhuyin = zhuyin[1:]

        if zhuyin in final_map:
            nucleus_seq = final_map[zhuyin]
        else:
            nucleus_seq = ''

        if onset == '' and zhuyin in final_map_alone:
            nucleus_seq = final_map_alone[zhuyin]

        nucleus = nucleus_seq[0] if nucleus_seq else 'ㅡ'
        coda = nucleus_seq[1:] if len(nucleus_seq) > 1 else ''

        result.append(combine_hangul(onset, nucleus, coda))
        if len(coda) > 0 and is_hangul_syllable(coda):
            result.append(coda)

    logging.info(f"zhuyin: {text} -> hangul: {''.join(result)}")

    return ''.join(result)
