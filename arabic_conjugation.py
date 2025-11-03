# Arabic conjugation core API
# Provides parsing and conjugation functions that can be reused by CLI/GUI

from typing import List, Tuple

# --- Unicode Constants for Arabic Harakat ---
FATHA = "\u064e"
DAMMA = "\u064f"
KASRA = "\u0650"
SUKUN = "\u0652"
SHADDA = "\u0651"
ALEF = "\u0627"
WAW = "\u0648"
YAA = "\u064a"
NOON = "\u0646"
TAA = "\u062a"
MEEM = "\u0645"
ALEF_MAKSURA = "\u0649"

HARAKAT = [FATHA, DAMMA, KASRA, SUKUN]

BABS = {
    "Fatha/Fatha (فَتَحَ / يَفْتَحُ)": (FATHA, FATHA),
    "Fatha/Damma (نَصَرَ / يَنْصُرُ)": (FATHA, DAMMA),
    "Fatha/Kasra (ضَرَبَ / يَضْرِبُ)": (FATHA, KASRA),
    "Kasra/Fatha (سَمِعَ / يَسْمَعُ)": (KASRA, FATHA),
    "Damma/Damma (كَرُمَ / يَكْرُمُ)": (DAMMA, DAMMA),
    "Kasra/Kasra (حَسِبَ / يَحْسِبُ)": (KASRA, KASRA),
}

MOODS = [
    ("Indicative (مرفوع)", "Indicative (مرفوع)"),
    ("Subjunctive (منصوب)", "Subjunctive (منصوب)"),
    ("Imperative (أمر)", "Imperative (أمر)"),
    ("Jussive (مجزوم)", "Jussive (مجزوم)"),
]


def parse_root(raw: str, reverse: bool = False) -> Tuple[str, str, str, str, str]:
    """Parse a 3-letter past-tense verb with harakat.

    Args:
        raw: input string (expected logical order, unless reverse=True)
        reverse: if True, reverse the characters before parsing (useful for display-ordered inputs)

    Returns: (F, A, L, hF, hA)

    Raises ValueError on parse error.
    """
    if raw is None:
        raise ValueError("No input provided")

    s = raw.strip()
    if reverse:
        s = s[::-1]

    # Keep only Arabic letters and harakat
    clean_input = "".join(c for c in s if "\u0600" <= c <= "\u06ff" or c in HARAKAT)
    letters_only = "".join(c for c in clean_input if c not in HARAKAT)

    if len(letters_only) < 3:
        raise ValueError("Input must contain at least three Arabic root letters with harakat")

    F, A, L = letters_only[0], letters_only[1], letters_only[2]

    def find_haraka(letter, start_index):
        idx = clean_input.find(letter, start_index)
        if idx != -1 and len(clean_input) > idx + 1 and clean_input[idx + 1] in HARAKAT:
            return clean_input[idx + 1], idx
        return None, -1

    # Find harakat for F and A as best-effort
    hF, idx_F = find_haraka(F, 0)
    hA = None
    if idx_F != -1:
        hA, _ = find_haraka(A, idx_F + 1)

    if hF is None:
        hF = FATHA
    if hA is None:
        raise ValueError("Could not detect the Haraka on the second root letter (A)")


    # Debug: print parsed root letters and their harakat
    print(f"F={F}, A={A}, L={L}, hF={hF}, hA={hA}")

    return F, A, L, hF, hA


def conjugate_past(F: str, A: str, L: str, hF: str, hA: str) -> List[str]:
    base_a = f"{F}{hF}{A}{hA}{L}"
    base_b = f"{F}{hF}{A}{FATHA}{L}{SUKUN}"
    forms = [
        f"{base_a}{FATHA}",
        f"{base_a}{FATHA}{ALEF}",
        f"{base_a}{DAMMA}{WAW}{SUKUN}{ALEF}",
        f"{base_a}{FATHA}{TAA}{SUKUN}",
        f"{base_a}{FATHA}{TAA}{ALEF}{FATHA}",
        f"{base_b}{NOON}{FATHA}",
        f"{base_b}{TAA}{FATHA}",
        f"{base_b}{TAA}{DAMMA}{MEEM}{FATHA}{ALEF}",
        f"{base_b}{TAA}{DAMMA}{MEEM}{SUKUN}",
        f"{base_b}{TAA}{KASRA}",
        f"{base_b}{TAA}{DAMMA}{MEEM}{FATHA}{ALEF}",
        f"{base_b}{TAA}{DAMMA}{NOON}{SHADDA}{FATHA}",
        f"{base_b}{TAA}{DAMMA}",
        f"{base_b}{NOON}{ALEF}",
    ]
    return forms


def conjugate_present(F: str, A: str, L: str, present_ayn_haraka: str, mood: str) -> List[str]:
    prefixes = [
        YAA,
        YAA,
        YAA,
        TAA,
        TAA,
        YAA,
        TAA,
        TAA,
        TAA,
        TAA,
        TAA,
        TAA,
        ALEF,
        NOON,
    ]
    stem = f"{F}{SUKUN}{A}{present_ayn_haraka}{L}"

    indicative_suffixes = [
        DAMMA,
        f"{FATHA}{ALEF}{NOON}{KASRA}",
        f"{DAMMA}{WAW}{SUKUN}{NOON}{FATHA}",
        DAMMA,
        f"{FATHA}{ALEF}{NOON}{KASRA}",
        f"{SUKUN}{NOON}{FATHA}",
        DAMMA,
        f"{FATHA}{ALEF}{NOON}{KASRA}",
        f"{DAMMA}{WAW}{SUKUN}{NOON}{FATHA}",
        f"{KASRA}{YAA}{SUKUN}{NOON}{FATHA}",
        f"{FATHA}{ALEF}{NOON}{KASRA}",
        f"{SUKUN}{NOON}{FATHA}",
        DAMMA,
        DAMMA,
    ]
    mood_rules = {
        "Indicative (مرفوع)": indicative_suffixes,
        "Subjunctive (منصوب)": [
            FATHA,
            f"{FATHA}{ALEF}",
            f"{DAMMA}{WAW}{SUKUN}{ALEF}",
            FATHA,
            f"{FATHA}{ALEF}",
            f"{SUKUN}{NOON}{FATHA}",
            FATHA,
            f"{FATHA}{ALEF}",
            f"{DAMMA}{WAW}{SUKUN}{ALEF}",
            f"{KASRA}{YAA}{SUKUN}",
            f"{FATHA}{ALEF}",
            f"{SUKUN}{NOON}{FATHA}",
            FATHA,
            FATHA,
        ],
        "Jussive (مجزوم)": [
            SUKUN,
            f"{FATHA}{ALEF}",
            f"{DAMMA}{WAW}{SUKUN}{ALEF}",
            SUKUN,
            f"{FATHA}{ALEF}",
            f"{SUKUN}{NOON}{FATHA}",
            SUKUN,
            f"{FATHA}{ALEF}",
            f"{DAMMA}{WAW}{SUKUN}{ALEF}",
            f"{KASRA}{YAA}",
            f"{FATHA}{ALEF}",
            f"{SUKUN}{NOON}{FATHA}",
            SUKUN,
            SUKUN,
        ],
    }

    if mood == "Imperative (أمر)":
        jussive_suffixes = mood_rules["Jussive (مجزوم)"]
        imperative_forms = []
        for i in range(14):
            if 6 <= i <= 11:
                imperative_forms.append(f"{ALEF}{present_ayn_haraka}{stem}{jussive_suffixes[i]}")
            else:
                imperative_forms.append("----")
        return imperative_forms

    current_suffixes = mood_rules.get(mood, mood_rules["Indicative (مرفوع)"])
    forms = [f"{prefixes[i]}{FATHA}{stem}{current_suffixes[i]}" for i in range(14)]
    return forms


def conjugate_verb(verb: str, tense: str = "past", bab_key: str = None, mood: str = None, reverse_input: bool = False) -> Tuple[str, List[str]]:
    """High-level API: given a verb string with harakat, produce title and 14 conjugations.

    Args:
        verb: input past-tense verb (string, with harakat)
        tense: 'past' or 'present'
        bab_key: when tense=='present', one of the keys of BABS (or shorthand handled by caller)
        mood: selected mood string from MOODS
        reverse_input: whether to reverse the input characters before parsing

    Returns: (title, list_of_14_forms)
    """
    F, A, L, hF, hA = parse_root(verb, reverse=reverse_input)
    if tense == "past":
        forms = conjugate_past(F, A, L, hF, hA)
        title = f"الماضي ({F}{hF}{A}{hA}{L}{FATHA})"
        return title, forms
    else:
        if bab_key is None:
            bab_key = list(BABS.keys())[0]
        _, present_ayn_haraka = BABS[bab_key]
        if mood is None:
            mood = "Indicative (مرفوع)"
        forms = conjugate_present(F, A, L, present_ayn_haraka, mood)
        title = f"المضارع - {mood} ({bab_key})"
        return title, forms
