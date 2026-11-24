from decimal import Decimal

from django.test import TestCase

from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from customers.models import Customer
from products.models import ProductColor, ProductImage
from store.models import Comment
from products.models import Brand, Category, Product

class ProductListAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.brand = Brand.objects.create(name="Rolex")
        self.category = Category.objects.create(
            title="Luxury",
            slug="luxury",
        )
        self.product = Product.objects.create(
            title="Submariner",
            slug="submariner",
            brand=self.brand,
            category=self.category,
            price=Decimal("2000.00"),
            description="A luxury watch",
            meta_title="Submariner",
            meta_description="Luxury watch",
        )

    def test_slug_is_generated_from_title_and_made_unique(self):
        category = Category.objects.create(title="New Arrivals")
        self.assertEqual(category.slug, "new-arrivals")

        products = [
            Product.objects.create(
                title="Automatic Watch",
                brand=self.brand,
                category=self.category,
                price=Decimal("1000.00"),
                description="A luxury watch",
                meta_title="Automatic Watch",
                meta_description="Luxury watch",
            )
            for _ in range(2)
        ]

        self.assertEqual(
            [product.slug for product in products],
            ["automatic-watch", "automatic-watch-1"],
        )

    def test_product_list_returns_product_with_brand_and_category(self):
        response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        product_data = response.data[0]
        self.assertEqual(
            set(product_data),
            {
                "id",
                "title",
                "slug",
                "price",
                "brand",
                "category",
                "is_available",
                "stash",
            },
        )
        self.assertEqual(product_data["title"], "Submariner")
        self.assertEqual(product_data["slug"], "submariner")
        self.assertEqual(product_data["price"], "2000.00")
        self.assertEqual(product_data["brand"]["name"], "Rolex")
        self.assertEqual(product_data["category"]["title"], "Luxury")
        self.assertTrue(product_data["is_available"])
        self.assertEqual(product_data["stash"], 0)

    def test_product_list_does_not_make_n_plus_one_queries(self):
        Product.objects.create(
            title="Datejust",
            slug="datejust",
            brand=self.brand,
            category=self.category,
            price=Decimal("3000.00"),
            description="A luxury watch",
            meta_title="Datejust",
            meta_description="Luxury watch",
        )
        Product.objects.create(
            title="Daytona",
            slug="daytona",
            brand=self.brand,
            category=self.category,
            price=Decimal("4000.00"),
            description="A luxury watch",
            meta_title="Daytona",
            meta_description="Luxury watch",
        )

        with self.assertNumQueries(1):
            response = self.client.get("/api/products/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)


    def test_product_detail_increments_click_count(self):
        response = self.client.get(
            f"/api/products/{self.product.slug}/"
        )

        self.assertEqual(response.status_code, 200)

        self.product.refresh_from_db()
        self.assertEqual(self.product.click_count, 1)
        self.assertEqual(response.data["click_count"], 1)

    def test_product_detail_returns_images_colors_and_comments(self):
        ProductImage.objects.create(
            product=self.product,
            image="products/test.jpg",
        )
        ProductColor.objects.create(
            product=self.product,
            color="Black",
            hex_code="#000000",
        )

        user = get_user_model().objects.create_user(username="commenter")
        customer = Customer.objects.create(user=user)
        Comment.objects.create(
            product=self.product,
            customer=customer,
            body="Great watch",
        )

        response = self.client.get(f"/api/products/{self.product.slug}/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["images"]), 1)
        self.assertEqual(len(response.data["colors"]), 1)
        self.assertEqual(len(response.data["comments"]), 1)
        self.assertEqual(response.data["comments"][0]["body"], "Great watch")

    def test_product_detail_does_not_make_n_plus_one_queries(self):
        for number in range(2):
            ProductImage.objects.create(
                product=self.product,
                image=f"products/test-{number}.jpg",
            )
            ProductColor.objects.create(
                product=self.product,
                color=f"Color {number}",
                hex_code=f"#00000{number}",
            )

        user = get_user_model().objects.create_user(username="detail-commenter")
        customer = Customer.objects.create(user=user)

        for number in range(2):
            Comment.objects.create(
                product=self.product,
                customer=customer,
                body=f"Comment {number}",
            )

        with self.assertNumQueries(8):
            response = self.client.get(
                f"/api/products/{self.product.slug}/"
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["images"]), 2)
        self.assertEqual(len(response.data["colors"]), 2)
        self.assertEqual(len(response.data["comments"]), 2)

    def test_luxury_special_returns_matching_products_and_average_price(self):
        Product.objects.create(
            title="Watch One",
            slug="watch-one",
            brand=self.brand,
            category=self.category,
            price=Decimal("2000.00"),
            is_special=True,
            is_luxury=True,
            is_available=True,
            description="A luxury watch",
            meta_title="Watch One",
            meta_description="Luxury watch",
        )
        Product.objects.create(
            title="Watch Two",
            slug="watch-two",
            brand=self.brand,
            category=self.category,
            price=Decimal("4000.00"),
            is_special=True,
            is_luxury=True,
            is_available=True,
            description="A luxury watch",
            meta_title="Watch Two",
            meta_description="Luxury watch",
        )
        Product.objects.create(
            title="Unavailable Watch",
            slug="unavailable-watch",
            brand=self.brand,
            category=self.category,
            price=Decimal("1000.00"),
            is_special=True,
            is_luxury=True,
            is_available=False,
            description="A luxury watch",
            meta_title="Unavailable Watch",
            meta_description="Luxury watch",
        )

        response = self.client.get("/api/luxury-special/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data["average_luxury_price"],
            Decimal("3000.00"),
        )
        self.assertEqual(len(response.data["products"]), 2)
        self.assertEqual(
            {item["title"] for item in response.data["products"]},
            {"Watch One", "Watch Two"},
        )
        self.assertEqual(
            set(response.data),
            {"average_luxury_price", "products"},
        )
        expected_product_fields = {
            "title",
            "price",
            "gender",
            "strap_material",
            "engine",
        }
        self.assertTrue(
            all(
                set(item) == expected_product_fields
                for item in response.data["products"]
            )
        )

    def test_luxury_special_excludes_non_special_and_non_luxury_products(self):
        Product.objects.create(
            title="Not Special",
            slug="not-special",
            brand=self.brand,
            category=self.category,
            price=Decimal("1000.00"),
            is_special=False,
            is_luxury=True,
            is_available=True,
            description="A watch",
            meta_title="Not Special",
            meta_description="A watch",
        )
        Product.objects.create(
            title="Not Luxury",
            slug="not-luxury",
            brand=self.brand,
            category=self.category,
            price=Decimal("1500.00"),
            is_special=True,
            is_luxury=False,
            is_available=True,
            description="A watch",
            meta_title="Not Luxury",
            meta_description="A watch",
        )

        response = self.client.get("/api/luxury-special/")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["average_luxury_price"], None)
        self.assertEqual(response.data["products"], [])