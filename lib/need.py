from api.models import *

from django.db import transaction

def insertTag(tags):
    try:
        tags = tags.split(",")
    except:
        pass

    for tag in tags:
        try:
            t = Tag.objects.get(name=tag)
        except:
            t = Tag.objects.create(name=tag)

    return True

def insertProducts(name, value, image, url):
    try:
        product = Products.objects.get_or_create(url=url)
    except:
        product = None

    if product != None:
        return False

    obj = product.update(name=name, value=value, image=image)

    return obj.id