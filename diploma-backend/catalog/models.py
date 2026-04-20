from django.db import models

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=200)
    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null = True,
        blank=True,
        related_name="subcategories"
    )
    image = models.ImageField(upload_to="categories/", blank=True, null=True)

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")
    tags = models.ManyToManyField(Tag, blank=True, related_name="products")

    title = models.CharField(max_length=255)
    description = models.TextField()
    full_description = models.TextField(blank=True)

    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    count = models.IntegerField(default=0)
    
    date = models.DateTimeField(auto_now_add=True)
    rating = models.FloatField(default=0.0)

    is_limited_edition = models.BooleanField(default=False)
    is_banner = models.BooleanField(default=False)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date']
        verbose_name = "Товар"
        verbose_name_plural = "Товары"

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="images"
    )
    image = models.ImageField(upload_to="products/")
    alt = models.CharField(max_length=255, blank=True)


class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    author = models.CharField(max_length=100)
    email = models.EmailField()
    text = models.TextField()
    rate = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"