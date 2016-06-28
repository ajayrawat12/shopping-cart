from .cart import Cart


def cart(request):
    """In our context processor, we instantiate
    the cart using the request object and make it available for the templates
    as a variable named cart."""

    return {'cart': Cart(request)}
