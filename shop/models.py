from django.db import models
from django.core.urlresolvers import reverse

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200,
                            db_index=True)
    slug = models.SlugField(max_length=200,
                            db_index=True,
                            unique=True)

    def get_absolute_url(self):
        """get_absolute_url() is the convention to retrieve URL
           for a given object."""

        return reverse('shop:product_list_by_category',args=[self.slug])

    class Meta:
        """docstring for Meta."""

        ordering = ('name',)
        verbose_name='category'
        verbose_name_plural = 'categories'

    def __unicode__(self):
        return self.name


class Product(models.Model):
    """ The Product model fields are as follows:
category: This is ForeignKey to the Category model. This is a many-to-one
relationship: A product belongs to one category and a category contains
multiple products."""

    category = models.ForeignKey(Category, related_name='products')
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        """As you already know, get_absolute_url() is the convention to retrieve URL
           for a given object. Here, we will use the URLs patterns
           that we just defined in the urls.py file."""

        return reverse('shop:product_detail', args=[self.id, self.slug])

    class Meta:
        """docstring for Meta."""

        ordering = ('name',)
        index_together = (('id', 'slug'),)

    def __unicode__(self):
        return self.name
