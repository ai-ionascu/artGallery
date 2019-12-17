from django.shortcuts import get_object_or_404
from paintings.models import Painting


def cart_contents(request):
    """
    Ensures that the cart contents are available when rendering every page
    """
    
    cart = request.session.get('cart', {})
    
    cart_items = []
    total = 0
    painting_count = 0
    for id, quantity in cart.items():
        painting = get_object_or_404(Painting, id=id)
        total += quantity * painting.price
        painting_count += quantity
        cart_items.append({'id':id, 'quantity': quantity, 'painting': painting})
        
    return { 'cart_items': cart_items, 'total': total, 'painting_count': painting_count }