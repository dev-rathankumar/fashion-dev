from django.db import models
from django.urls import reverse

# Image manipulation
from io import BytesIO
from PIL import Image
from django.core.files import File

from mptt.models import MPTTModel, TreeForeignKey


# Image compression method
def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image

class Category(MPTTModel):
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    category_name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    cat_image = models.ImageField(upload_to='store/categories/%Y/%m/%d', blank=True)
    is_active       = models.BooleanField(default=True)
    created_date    = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.category_name

    class MPTTMeta:
        order_insertion_by = ['category_name']

    def __str__(self):
        full_path = [self.category_name]
        k = self.parent
        while k is not None:
            full_path.append(k.category_name)
            k = k.parent
        return ' / '.join(full_path[::-1])

    # Override save method
    # def save(self, *args, **kwargs):
    #     new_image = compress(self.cat_image)
    #     self.cat_image = new_image
    #     super(Category, self).save(*args, **kwargs)
    #     img = Image.open(self.cat_image.path)
    #     if img.height > 300 or img.width > 300:
    #         output_size = (300,300)
    #         img.thumbnail(output_size)
    #         img.save(self.cat_image.path)
    #     super(Category, self).save(*args, **kwargs)

    # def get_url(self):
    #         return reverse('products_by_category', args=[self.slug])
