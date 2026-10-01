import textstat

threshold_r = 2.1


def readability_drop(original, candidate):
    return textstat.flesch_kincaid_grade(original) - textstat.flesch_kincaid_grade(candidate)


def readable(original, candidate, threshold=threshold_r):
    return readability_drop(original, candidate) >= threshold