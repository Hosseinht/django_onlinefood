import os.path

from django.core.exceptions import ValidationError


def image_validator(value):
    extension = os.path.splitext(value.name)[1]
    valid_extensions = [".png", ".jpg", ".jpeg"]
    if not extension.lower() in valid_extensions:
        raise ValidationError(
            "Unsupported file extensions. Allowed extensions: " + str(valid_extensions)
        )
