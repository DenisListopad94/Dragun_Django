from django.forms import ValidationError


def validate_yahoo_email(value) -> None:
    if "yahoo.com" not in value:
        raise ValidationError("Email must be a yahoo.com email address.")
    

def validate_doc_extension(value):
    if not value.name.endswith('.doc'):
        raise ValidationError('Only doc format.')