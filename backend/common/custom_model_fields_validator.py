from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as lazy_load
import os
from django.utils.deconstruct import deconstructible
import magic

def validate_file_extension_and_size(valid_extensions, size_limit):
    
    def validator(value):
        ext = os.path.splitext(value.name)[1]  # Get file extension
        # valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']  # Add your valid extensions here
        if not ext.lower() in valid_extensions:
            raise ValidationError(lazy_load('Unsupported file extension.'))

        if value.size > size_limit:
            raise ValidationError(lazy_load('File size exceeds the allowed limit of 1MB.'))
            
    return validator
    
def validate_file_mime_type(valid_mime_types):

    def validator(value):
         
        # valid_mime_types = ['image/jpeg', 'image/png', 'application/pdf']  # Add your valid MIME types here
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(value.read())
        
        if file_mime_type not in valid_mime_types:
            raise ValidationError(lazy_load('Unsupported file type.'))
        
        value.seek(0)  # Reset file pointer to the beginning

    return validator


# Class based validator
@deconstructible
class FileSizeValidator:
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, value):
        if value.size > self.max_size:
            raise ValidationError(lazy_load('File size exceeds the allowed limit of {0} bytes').format(self.max_size))
    
    def __eq__(self, other):
        return (
            isinstance(other, FileSizeValidator)
            and (self.max_size == other.max_size)

        )
@deconstructible      
class FileExtensionValidator:
    def __init__(self, file_extensions):
          self.file_extensions = file_extensions
    def __call__(self, value):
        ext = os.path.splitext(value.name)[1]  # Get file extension
        # valid_extensions = ['.jpg', '.jpeg', '.png', '.pdf']  # Add your valid extensions here
        if not ext.lower() in self.file_extensions:
            raise ValidationError(lazy_load('Unsupported file extension.'))
    def __eq__(self, other):
        return (
            isinstance(other, FileExtensionValidator)
            and (self.file_extensions == other.file_extensions)

        )
        
@deconstructible
class FileMimeTypeValidator:
    def __init__(self, mime_types):
        self.mime_types = mime_types
    
    def __call__(self, value):
        mime = magic.Magic(mime=True)
        file_mime_type = mime.from_buffer(value.read())
        
        if file_mime_type not in self.mime_types:
            raise ValidationError(lazy_load('Unsupported file type.'))
        
        value.seek(0)  # Reset file pointer to the beginning
    
    def __eq__(self, other):
        return (
            isinstance(other, FileMimeTypeValidator)
            and (self.mime_types == other.mime_types)

        )
