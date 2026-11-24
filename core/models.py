from django.db import models
from django.utils.text import slugify


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SluggedMixinModel(models.Model):
    slug = models.SlugField(max_length=255, unique=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            slug_field = self._meta.get_field("slug")
            max_length = slug_field.max_length
            base_slug = slugify(self.title) or self._meta.model_name
            base_slug = base_slug[:max_length]
            candidate = base_slug
            existing_slugs = type(self)._default_manager.all()
            if self.pk is not None:
                existing_slugs = existing_slugs.exclude(pk=self.pk)

            suffix = 1
            while existing_slugs.filter(slug=candidate).exists():
                suffix_text = f"-{suffix}"
                candidate = (
                    f"{base_slug[:max_length - len(suffix_text)]}{suffix_text}"
                )
                suffix += 1

            self.slug = candidate
            if kwargs.get("update_fields") is not None:
                kwargs["update_fields"] = set(kwargs["update_fields"]) | {"slug"}

        super().save(*args, **kwargs)

    class Meta:
        abstract = True