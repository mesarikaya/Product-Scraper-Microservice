import logging
import re


def apply_regex(text, regex, offset_left, offset_right):
    try:
        match = re.search(regex, text)
        start = int(match.start()) + offset_left
        end = int(match.end()) - offset_right
    except IndexError as e:
        logging("Error with start and stop indices:", e, "with regex:", regex)
        return ""
    except Exception as e:
        logging.info("Exception in searching text:", e, "with regex:", regex)
        return ""
    else:
        return text[start:end]
