from django.db import models
from core.models import BaseModel, SluggedMixinModel

class Brand(BaseModel):
    name = models.CharField(max_length=150)
    meta_title = models.CharField(max_length=255, blank=True)
    meta_description = models.TextField(blank=True)


class Category(BaseModel, SluggedMixinModel):
    title = models.CharField(max_length=150)


class Product(BaseModel, SluggedMixinModel):
    
    class GenderChoices(models.TextChoices):
        MEN = "men", "Men"
        WOMEN = "women", "Women"
        UNISEX = "unisex", "Unisex"

    class OriginChoices(models.TextChoices):
        SWISS = "switzerland", "Switzerland"
        GERMANY = "germany", "Germany"
        JAPAN = "japan", "Japan"
        ITALY = "italy", "Italy"
        USA = "usa", "USA"
        FRANCE = "france", "France"
        OTHER = "other", "Other"

    class StrapMaterialChoices(models.TextChoices):
        LEATHER = "leather", "Leather"
        METAL = "metal", "Metal"
        RUBBER = "rubber", "Rubber"
        SILICONE = "silicone", "Silicone"

    class UsageChoices(models.TextChoices):
        DAILY = "daily", "Daily"
        SPORT = "sport", "Sport"
        LUXURY = "luxury", "Luxury"
        FORMAL = "formal", "Formal"
        CASUAL = "casual", "Casual"

    class DesignChoices(models.TextChoices):
        CLASSIC = "classic", "Classic"
        MODERN = "modern", "Modern"
        SPORTY = "sporty", "Sporty"
        MINIMAL = "minimal", "Minimal"

    class EngineChoices(models.TextChoices):
        AUTOMATIC = "automatic", "Automatic"
        QUARTZ = "quartz", "Quartz"
        MECHANICAL = "mechanical", "Mechanical"
        SOLAR = "solar", "Solar"

    title = models.CharField(max_length=200)
    
    brand = models.ForeignKey(
        Brand,
        on_delete=models.PROTECT,
        related_name="products",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="products",
    )

    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    is_discount = models.BooleanField(default=False)
    
    is_available = models.BooleanField(default=True)
    
    is_special = models.BooleanField(default=False)

    gender = models.CharField(
        max_length=20,
        choices=GenderChoices.choices,
        default=GenderChoices.UNISEX,
    )
    origin = models.CharField(
        max_length=20,
        choices=OriginChoices.choices,
        default=OriginChoices.SWISS,
    )
    strap_material = models.CharField(
        max_length=20,
        choices=StrapMaterialChoices.choices,
        default=StrapMaterialChoices.LEATHER,
    )
    usage = models.CharField(
        max_length=20,
        choices=UsageChoices.choices,
        default=UsageChoices.DAILY,
    )
    design = models.CharField(
        max_length=20,
        choices=DesignChoices.choices,
        default=DesignChoices.CLASSIC,
    )
    engine = models.CharField(
        max_length=20,
        choices=EngineChoices.choices,
        default=EngineChoices.QUARTZ,
    )

    main_image = models.ImageField(
        upload_to="products/",
        default="products/default.jpg"
    )

    features = models.JSONField(
        default=dict
    )

    is_luxury = models.BooleanField(default=False)

    description = models.TextField()

    meta_title = models.CharField(
        max_length=255
    )

    meta_description = models.TextField()

    stash = models.PositiveIntegerField(default=0)

    click_count = models.PositiveIntegerField(default=0)


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/images/")


class ProductColor(BaseModel):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="colors"
    )
    color = models.CharField(max_length=50)
    hex_code = models.CharField(max_length=7)