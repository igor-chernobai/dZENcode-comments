from celery import shared_task
from PIL import Image

from comments.models import Comment


@shared_task
def resize_img(comment_id: int):
    max_size = (320, 240)
    obj = Comment.objects.get(id=comment_id)
    img = Image.open(obj.image.path)

    img.thumbnail(max_size)
    img.save(obj.image.path)
