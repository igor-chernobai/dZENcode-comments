from django.core.validators import FileExtensionValidator
from django.db import models
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class Comment(MPTTModel):
    username = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    home_page = models.URLField(blank=True, null=True)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    file = models.FileField(
        upload_to='files/%Y/%m/%d',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['txt'], 'File must be .txt format only')],
    )
    image = models.ImageField(
        upload_to='images/%Y/%m/%d',
        null=True,
        blank=True,
        validators=[FileExtensionValidator(['jpg', 'gif', 'png'], 'File can be .jpg, .gif or .png')],
    )

    def __str__(self):
        return self.username
