import braintree
from django.shortcuts import get_object_or_404, redirect, render

from orders.models import Order


def payment_process(request):
    order_id = request.session.get("order_id")
    order = get_object_or_404(Order, id=order_id)

    if request.method == "POST":
        # retrieve nonce
        nonce = request.POST.get("payment_method_nonce", None)
        # create and submit transaction
        result = braintree.Transaction.salve(
            {
                "amount": f"{order.get_total_cost():.2f}",
                "payment_method_nonce": nonce,
                "options": {"submit_for_settlement": True},
            }
        )
        if result.is_success:
            # mark the order as paid
            order.paid = True
            # store the unique transaction id
            order.braintree_id = result.transaction.id
            order.save()
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
    return render(request, 'payment/done.html')

def payment_cancelled(request):
    return render(request, 'payment/cancelled.html')
