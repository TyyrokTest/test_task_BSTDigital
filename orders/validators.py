from django.core.exceptions import ValidationError
import re

def validate_serial(value):
    """Validate format of provided serial -'R2-D2', 'D3-23' """
    if not re.match("^\w{2}-\w{2}$", value):
        raise ValidationError(
            "Серийный номер должен состоять только из цифр, букв и быть в формате 'R2-D2'",
            params={"value": value},
        )