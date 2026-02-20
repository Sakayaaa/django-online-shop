from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from products.models import Brand, Category, Product

from .models import CartItem


class CartQuantityViewsTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email="user@example.com",
            password="test-pass-123",
        )
        self.client.force_login(self.user)

        self.category = Category.objects.create(name="Phones")
        self.brand = Brand.objects.create(name="Apple")
        self.product = Product.objects.create(
            name="iPhone 17",
            category=self.category,
            brand=self.brand,
            price="999.99",
        )

    def test_add_same_product_twice_keeps_quantity_one(self):
        url = reverse("add", kwargs={"slug": self.product.slug})

        self.client.get(url)
        self.client.get(url)

        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, 1)

    def test_increase_quantity_increments_existing_item(self):
        add_url = reverse("add", kwargs={"slug": self.product.slug})
        increase_url = reverse("increase-quantity", kwargs={"slug": self.product.slug})

        self.client.get(add_url)
        self.client.get(increase_url)

        self.assertEqual(CartItem.objects.count(), 1)
        self.assertEqual(CartItem.objects.get().quantity, 2)

    def test_decrease_quantity_reduces_and_removes_item(self):
        add_url = reverse("add", kwargs={"slug": self.product.slug})
        increase_url = reverse("increase-quantity", kwargs={"slug": self.product.slug})
        decrease_url = reverse("decrease-quantity", kwargs={"slug": self.product.slug})

        self.client.get(add_url)
        self.client.get(increase_url)
        self.client.get(decrease_url)

        self.assertEqual(CartItem.objects.get().quantity, 1)

        self.client.get(decrease_url)

        self.assertFalse(CartItem.objects.exists())

    def test_increase_quantity_supports_next_redirect(self):
        add_url = reverse("add", kwargs={"slug": self.product.slug})
        increase_url = reverse("increase-quantity", kwargs={"slug": self.product.slug})
        cart_url = reverse("cart-view")

        self.client.get(add_url)
        response = self.client.get(f"{increase_url}?next={cart_url}")

        self.assertRedirects(response, cart_url)
        self.assertEqual(CartItem.objects.get().quantity, 2)

    def test_decrease_quantity_supports_next_redirect(self):
        add_url = reverse("add", kwargs={"slug": self.product.slug})
        decrease_url = reverse("decrease-quantity", kwargs={"slug": self.product.slug})
        cart_url = reverse("cart-view")

        self.client.get(add_url)
        response = self.client.get(f"{decrease_url}?next={cart_url}")

        self.assertRedirects(response, cart_url)
        self.assertFalse(CartItem.objects.exists())
