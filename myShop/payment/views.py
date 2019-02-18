from io import BytesIO

import braintree
import weasyprint
from django.conf import settings
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404, redirect, render
from django.template.loader import render_to_string

from orders.models import Order
from shop.recommender import Recommender


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # retrieve nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction
        result = braintree.Transaction.sale(
            {
                "amount": f"{order.get_total_cost():.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            recommender = Recommender()
            recommender.products_bought(order.items.all())

            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()

            # create invoice email
            subject = f"My Shop - Invoice No. {order.id}"
            msg = "Please, find attached the invoice for your recent purchase"
            email = EmailMessage(
                subject, msg, "admin@myshop.com", [order.email]
            )

            # generate PDF
            html = render_to_string("orders/order/pdf.html", {"order": order})
            out = BytesIO()
            static_root = settings.STATIC_ROOT
            stylesheets = [weasyprint.CSS(f"{static_root}css/pdf.css")]
            weasyprint.HTML(string=html).write_pdf(
                out, stylesheets=stylesheets
            )

            # attach PDF file
            email.attach(
                f"order_{order.id}.pdf", out.getvalue(), "application/pdf"
            )

            # send email
            email.send()

            return redirect("payment:done")
        else:
            return redirect("payment:cancelled")
    else:
        # generate token
        client_token = braintree.ClientToken.generate()
        return render(
            request,
            "payment/process.html",
            {"client_token": client_token, "order": order},
        )


def payment_done(request):
    return render(request, "payment/done.html")


def payment_cancelled(request):
    return render(request, "payment/cancelled.html")
