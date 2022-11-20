from django.db import models


class Item(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField(default=0)  # Hundredths of currency

    class Meta:
        verbose_name = 'Item'
        verbose_name_plural = 'Items'

    def get_display_price(self):
        return "{0:.2f}".format(self.price / 100)

    def __str__(self):
        return '{}'.format(self.name)


class Order(models.Model):
    paid = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Order'
        verbose_name_plural = 'Orders'

    def __str__(self):
        return 'Order {}'.format(self.id)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.PROTECT)
    item = models.ForeignKey(Item, related_name='order_items', on_delete=models.PROTECT)

    def __str__(self):
        return '{}'.format(self.id)
