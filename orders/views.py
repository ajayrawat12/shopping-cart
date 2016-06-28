"""views for the Order ."""
from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
#from .tasks import order_created
from .models import Order
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required

from django.conf import settings
from django.http import HttpResponse
from django.template.loader import render_to_string
#import weasyprint
from weasyprint import HTML, CSS
#import os
from django.core.mail import send_mail
# from decimal import Decimal


# Create your views here.

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html', {'order': order})


@staff_member_required
def admin_order_pdf(request, order_id):
    # import ipdb
    # ipdb.set_trace()
    # cart = Cart(request)
    order = get_object_or_404(Order, id=order_id)

    # if cart.coupon:
    #     order.discount = cart.coupon.discount   'order_discount': order.discount, 

    html = render_to_string('orders/order/pdf.html', {'order': order,})
    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = 'filename= "order_{}.pdf" '.format(order.id)
    # ,stylesheets=[weasyprint.CSS(os.path.join(settings.STATIC_ROOT, 'css/pdf.css')])
    HTML(string=html).write_pdf(response,
        stylesheets=[CSS(settings.STATIC_ROOT + 'css\pdf.css')])
    return response




def order_create(request):

    #we will obtain the current cart from the session with cart = Cart(request).

    cart = Cart(request)

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()

            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
                cart.clear()

                #We call the delay() method of the task to execute it asynchronously. The task will
                #be added to the queue and will be executed by a worker as soon as possible.
                # order_created.delay(order.id)

                from_email = settings.EMAIL_HOST_USER
                subject = 'Order nr. {}'.format(order.id)
                message = 'Dear {},\n\nYou have successfully placed an order. \
                    Your order id is {}.'.format(order.first_name, order.id)
                send_mail(subject, message, from_email, [order.email], fail_silently=True)

                return render(request, 'orders/order/created.html',
                              {'order': order})
    else:
        form = OrderCreateForm()

    return render(request, 'orders/order/create.html', {'cart': cart,
                  'form': form})
