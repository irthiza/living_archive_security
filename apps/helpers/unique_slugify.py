from django.utils.crypto import get_random_string
from django.utils.text import slugify
import uuid


def unique_slug_generator(instance, field_to_slug='name', new_slug=None):
    if not getattr(instance, field_to_slug):
        return slugify(uuid.uuid4())
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(getattr(instance, field_to_slug))

    Klass = instance.__class__

    while Klass.objects.filter(slug=slug).exists():
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz')
        )
        return unique_slug_generator(instance, field_to_slug, new_slug=new_slug)
    return slug
