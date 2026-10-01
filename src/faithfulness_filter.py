from summac.model_summac import SummaCZS
model_CZS = SummaCZS(granularity="sentence", model_name="vitc")


#generated dictionary of modals and their categories, sorted with shall not before shall

MODAL_LEXICON = {

    "shall not": "prohibition",
    "must not": "prohibition",
    "may not": "prohibition",
    "will not": "prohibition",
    "won't": "prohibition",
    "cannot": "prohibition",
    "can not": "prohibition",
    "can't": "prohibition",

    "need not": "no_obligation",
    "does not have to": "no_obligation",
    "do not have to": "no_obligation",
    "is not required to": "no_obligation",
    "are not required to": "no_obligation",

    "is required to": "obligation",
    "are required to": "obligation",
    "has to": "obligation",
    "have to": "obligation",
    "needs to": "obligation",
    "need to": "obligation",
    "shall": "obligation",
    "must": "obligation",
    "will": "obligation",

    "may": "permission",
    "can": "permission",

    "should": "recommendation",
}



def get_modals(text):
    text = text.lower().replace("’", "'")
    for mark in ".,;:()\"":
        text = text.replace(mark, " ")
    text = " " + " ".join(text.split()) + " "
    # adds space in the beginning and in the end so that later the first and last word wont be ignored

    classes = set()
    for phrase, category in MODAL_LEXICON.items():
        if " " + phrase + " " in text:
            classes.add(category)
            text = text.replace(" " + phrase + " ", " ")
    return classes


def modal_flip_detected(original, candidate):
    return get_modals(original) != get_modals(candidate)


#faithful_min  = 0.316772 corrupted_max = -0.000896
#threshold = (0.316772 + (-0.000896)) / 2 = 0.315876 / 2 ≈ 0.158
#faithful_min  = 0.800545 corrupted_max = 0.002337
#threshold = (0.800545 + 0.002337) / 2 = 0.802882 / 2 ≈ 0.401
def is_faithful(original, candidate, threshold_foward = 0.16 , threshold_reverse = 0.4):
    has_modal_flip = modal_flip_detected(original, candidate)

    forward_score = model_CZS.score([original], [candidate])["scores"][0]
    reverse_score = model_CZS.score([candidate], [original])["scores"][0]
    forward_ok = False
    reverse_ok = False
    if forward_score >= threshold_foward: forward_ok = True
    if reverse_score >= threshold_reverse: reverse_ok = True

    faith = False
    #if has_modal_flip==False and forward_ok and reverse_ok: faith=True
    if has_modal_flip == False and forward_ok:
        faith = True
    return {
        "is_faithful": faith,
        "modal_flip": has_modal_flip,
        "forward_score": forward_score,
        "reverse_score": reverse_score,
    }
