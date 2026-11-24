from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from customers.models import Customer
from products.models import Brand, Category, Product
from .models import WishList

class WishlistAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        User = get_user_model()

        self.user1 = User.objects.create_user(
            username="user1",
            email="user1@example.com",
            password="test-password",
        )
        self.user2 = User.objects.create_user(
            username="user2",
            email="user2@example.com",
            password="test-password",
        )

        self.customer1 = Customer.objects.create(
            user=self.user1,
            phone_number="09120000001",
        )
        self.customer2 = Customer.objects.create(
            user=self.user2,
            phone_number="09120000002",
        )

        brand = Brand.objects.create(name="Rolex")
        category = Category.objects.create(
            title="Luxury",
            slug="luxury",
        )
        self.product = Product.objects.create(
            title="Submariner",
            slug="submariner",
            brand=brand,
            category=category,
            price=Decimal("2000.00"),
            description="A luxury watch",
            meta_title="Submariner",
            meta_description="Luxury watch",
        )
        
    def test_wishlist_returns_product(self):
        WishList.objects.create(
            customer=self.customer1,
            product=self.product,
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/me/wishlist/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        item = response.data[0]
        self.assertEqual(
            set(item),
            {"product", "customer"},
        )
        self.assertEqual(
            set(item["product"]),
            {"title", "slug", "price", "stash", "main_image"},
        )
        self.assertEqual(item["product"]["title"], "Submariner")
        self.assertEqual(item["product"]["slug"], "submariner")
        self.assertEqual(item["product"]["price"], "2000.00")
        self.assertEqual(item["product"]["stash"], 0)
        self.assertTrue(
            item["product"]["main_image"].endswith("products/default.jpg")
        )
        self.assertEqual(
            set(item["customer"]),
            {"username", "email", "phone_number"},
        )
        self.assertEqual(item["customer"]["username"], "user1")
        self.assertEqual(item["customer"]["email"], "user1@example.com")
        self.assertEqual(item["customer"]["phone_number"], "09120000001")

    def test_wishlist_requires_authentication(self):
        response = self.client.get("/api/me/wishlist/")

        self.assertIn(response.status_code, [401, 403])

    def test_wishlist_returns_only_current_users_items(self):
        WishList.objects.create(
            customer=self.customer1,
            product=self.product,
        )
        WishList.objects.create(
            customer=self.customer2,
            product=self.product,
        )

        self.client.force_authenticate(user=self.user1)
        response = self.client.get("/api/me/wishlist/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(
            response.data[0]["customer"]["username"],
            self.user1.username,
        )

    def test_wishlist_query_count_does_not_grow_with_item_count(self):
        for number in range(2):
            product = Product.objects.create(
                title=f"Watch {number}",
                slug=f"watch-{number}",
                brand=self.product.brand,
                category=self.product.category,
                price=Decimal("2500.00"),
                description="A luxury watch",
                meta_title=f"Watch {number}",
                meta_description="Luxury watch",
            )
            WishList.objects.create(
                customer=self.customer1,
                product=product,
            )
        WishList.objects.create(
            customer=self.customer1,
            product=self.product,
        )

        self.client.force_authenticate(user=self.user1)
        with self.assertNumQueries(1):
            response = self.client.get("/api/me/wishlist/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)