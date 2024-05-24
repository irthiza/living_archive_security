from django.utils.crypto import get_random_string


def unique_code_generator(instance, new_code=None):
    if new_code is not None:
        code = new_code
    else:
        code = get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz')

    Klass = instance.__class__

    while Klass.objects.filter(code=code).exists():
        new_code = "{code}-{randstr}".format(
            code=code,
            randstr=get_random_string(length=6, allowed_chars='abcdefghijklmnopqrstuvwxyz')
        )
        return unique_code_generator(instance, new_code=new_code)
    return code
