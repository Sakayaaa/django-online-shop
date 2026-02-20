from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.utils.http import url_has_allowed_host_and_scheme
from django.views import View

from .models import Cart, CartItem
from products.models import Product


def _redirect_after_quantity_change(request, product_slug):
    next_url = request.GET.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url,
        allowed_hosts={request.get_host()},
        require_https=request.is_secure(),
    ):
        return redirect(next_url)
    return redirect("products:product_detail", slug=product_slug)

class CartView(LoginRequiredMixin, View):
    def get(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        items = cart.items.select_related("product").all()

        return render(request, "checkout/cart.html", {"cart": cart, "items": items})


class Add(LoginRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": 1},
        )

        return _redirect_after_quantity_change(request, product.slug)


class IncreaseQuantity(LoginRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={"quantity": 1},
        )
        if not created:
            item.quantity += 1
            item.save(update_fields=["quantity"])

        return _redirect_after_quantity_change(request, product.slug)


class DecreaseQuantity(LoginRequiredMixin, View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        item = CartItem.objects.filter(cart=cart, product=product).first()

        if item:
            if item.quantity > 1:
                item.quantity -= 1
                item.save(update_fields=["quantity"])
            else:
                item.delete()

        return _redirect_after_quantity_change(request, product.slug)
