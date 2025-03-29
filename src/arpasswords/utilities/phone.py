import re

from ..exceptions import PhoneNotCorrect


def format(phone: str) -> str:
    digits: str = re.sub(r"\D", "", phone)
    if len(digits) == 11:
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"
    elif len(digits) == 10:
        return f"+7 ({digits[0:3]}) {digits[3:6]}-{digits[6:8]}-{digits[8:]}"
    raise PhoneNotCorrect()
