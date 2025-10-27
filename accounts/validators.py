import re
from django.core.exceptions import ValidationError


def house_number_validator(value):
    pattern = r'^\d{1,3}(/[\d]{1,2})?$'
    if not re.match(pattern, value):
        raise ValidationError(
            'Invalid House Number. Valid Examples: 2, 24, 246, 24/1, ... (max length is 5 characters)'
        )
