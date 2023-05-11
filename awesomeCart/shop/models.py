from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name= models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    sub_category = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=300)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self):
        # this method will no more show product object in database, it will show product name like watch
        return self.product_name
    
class Contact(models.Model):
    msg_id = models.AutoField(primary_key=True)
    name= models.CharField(max_length=50)
    email = models.CharField(max_length=50, default="")
    query = models.CharField(max_length=500, default="")
    

    def __str__(self):
        
        return self.name
    # after building a class in model , makemigrations , then migrate 
    # then register model in admin. py 
    # makemigrations se migrations bante he and migrate se migrate hote he 


class Orders(models.Model):
    order_id = models.AutoField(primary_key=True)
    items_json = models.CharField(max_length=50000)
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=90)
    address = models.CharField(max_length=90)
    city = models.CharField(max_length=90)
    state = models.CharField(max_length=90)
    zip_code = models.CharField(max_length=90) 
    phone = models.CharField(max_length=111, default="")

    # def __str__(self):
    #     return self.order_id
class OrderUpdate(models.Model):
    update_id= models.AutoField(primary_key=True)
    order_id= models.IntegerField(default="")
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
    