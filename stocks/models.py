from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class StocksModel(models.Model):
    stock_name = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10)
    price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    pe_ratio = models.FloatField(null=True)
    volume = models.IntegerField(null=True)
    market_cap = models.FloatField(null=True)

    def __str__(self):
        return self.stock_name

    
class UserQueryModel(models.Model):
    user = models.ForeignKey(User,related_name='user', on_delete=models.CASCADE)
    stocks = models.ForeignKey(StocksModel,related_name='stocks', on_delete=models.CASCADE)
    query = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user} : {self.stocks}'
    
