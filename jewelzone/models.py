from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):

    fname = models.CharField(max_length=50)
    lname = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    mobile = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    cpassword = models.CharField(max_length=50)
    usertype = models.CharField(max_length=50,default="user")
    user_image = models.ImageField(upload_to='user_image/',default='')

    def __str__(self):
        return self.fname + " " + self.lname

class Contact(models.Model):

    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    telephone = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name

class Gold_jewelry(models.Model):

    CHOICES = (
        ("rings",'rings'),
        ("necklace",'necklace'),
        ("earrings",'earrings'),
        ("pendants",'pendants'),
        ("bangles",'bangles'),
        ("bracelet",'bracelet'),
        ("chains",'chains'),
    )

    METAL_COLOUR = (
        ("yellow",'yellow'),
        ("rose",'rose'),
        ("two_tone",'two_tone'),
    )

    GENDER = (
        ("men",'men'),
        ("women",'women'),
    )

    # SIZES = (
    #     ("9",'9'),
    #     ("10",'10'),
    #     ("11",'11'),
    #     ("12",'12'),
    #     ("13",'13'),
    #     ("14",'15'),
    #     ("16",'16'),
    #     ("2.2",'2.2'),
    #     ("2.3",'2.3'),
    #     ("2.4",'2.4'),
    #     ("2.5",'2.5'),
    #     ("2.6",'2.6'),
    #     ("2.7",'2.7'),
    #     ("2.8",'2.8'),
    #     ("2.9",'2.9'),
    #     ("2.10",'2.10'),
    #     ("2.11",'2.11'),
    #     ("2.12",'2.12'),
    # )

    gold_category = models.CharField(max_length=50,choices=CHOICES,default="")
    gold_name = models.CharField(max_length=40)
    gold_des_code = models.CharField(max_length=10)
    gold_price = models.CharField(max_length=10)
    gold_gross = models.CharField(max_length=10)
    gold_net = models.CharField(max_length=10)
    gold_stone_wt = models.CharField(max_length=10,default="")
    # gold_size = models.CharField(max_length=5,default="")
    gold_gender = models.CharField(max_length=20,choices=GENDER)
    gold_metal_colour = models.CharField(max_length=50,choices=METAL_COLOUR)
    gold_purity = models.CharField(max_length=10,default="22KT (916)")
    gold_certification = models.CharField(max_length=20,default="BIS Hallmark 916")
    gold_stock = models.CharField(max_length=20,default="Available")
    gold_image = models.ImageField(upload_to='gold_jewelry',default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.fname + " -- " +self.gold_name

class Diamond_jewelry(models.Model):

    CHOICES = (
        ("rings",'rings'),
        ("necklace",'necklace'),
        ("earrings",'earrings'),
        ("pendants",'pendants'),
        ("bangles",'bangles'),
        ("bracelet",'bracelet'),
    )

    METAL_COLOUR = (
        ("white",'white'),
        ("yellow",'yellow'),
        ("rose",'rose'),
        ("two_tone",'two_tone'),
    )

    GENDER = (
        ("men",'men'),
        ("women",'women'),
    )

    diamond_category = models.CharField(max_length=50,choices=CHOICES,default="")
    diamond_name = models.CharField(max_length=40)
    diamond_des_code = models.CharField(max_length=10)
    diamond_price = models.CharField(max_length=10)
    diamond_gross = models.CharField(max_length=10)
    diamond_net = models.CharField(max_length=10)
    # gold_size = models.CharField(max_length=5,default="")
    diamond_gender = models.CharField(max_length=20,choices=GENDER,default="")
    diamond_metal_colour = models.CharField(max_length=50,choices=METAL_COLOUR,default="")
    diamond_gold_purity = models.CharField(max_length=10,default="18KT (750)")
    diamond_gold_certification = models.CharField(max_length=20,default="BIS Hallmark 750")
    diamond_certification = models.CharField(max_length=20,default="IGI")
    diamond_stock = models.CharField(max_length=20,default="Available")
    diamond_image = models.ImageField(upload_to='diamond_jewelry',default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.fname + " -- " +self.diamond_name


class Platinum_jewelry(models.Model):

    CHOICES = (
        ("rings",'rings'),
        ("necklace",'necklace'),
        ("earrings",'earrings'),
        ("pendants",'pendants'),
        ("bracelet",'bracelet'),
        ("chains",'chains')
    )

    METAL_COLOUR = (
        ("platinum",'platinum'),
        ("two_tone",'two_tone'),
    )

    GENDER = (
        ("men",'men'),
        ("women",'women'),
    )

    platinum_category = models.CharField(max_length=50,choices=CHOICES,default="")
    platinum_name = models.CharField(max_length=40)
    platinum_des_code = models.CharField(max_length=10)
    platinum_price = models.CharField(max_length=10)
    platinum_gross = models.CharField(max_length=10)
    platinum_net = models.CharField(max_length=10)
    # gold_size = models.CharField(max_length=5,default="")
    platinum_gender = models.CharField(max_length=20,choices=GENDER,default="")
    platinum_metal_colour = models.CharField(max_length=50,choices=METAL_COLOUR,default="")
    platinum_purity = models.CharField(max_length=10,default="PT (950)")
    platinum_certification = models.CharField(max_length=10,default="PGI")
    platinum_diamond_certification = models.CharField(max_length=10,default="IGI")
    platinum_stock = models.CharField(max_length=10,default="Available")
    platinum_image = models.ImageField(upload_to='diamond_jewelry',default="")
    user = models.ForeignKey(User,on_delete=models.CASCADE,default="",null=True,blank=True)

    def __str__(self):
        return self.user.fname + " -- " +self.platinum_name

class Cart(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    gold_jew = models.ForeignKey(Gold_jewelry,on_delete=models.CASCADE,null=True)
    dia_jew = models.ForeignKey(Diamond_jewelry,on_delete=models.CASCADE,null=True)
    pt_jew = models.ForeignKey(Platinum_jewelry,on_delete=models.CASCADE,null=True)
    added_date = models.DateField(default=timezone.now)
    total_price = models.IntegerField()
    total_qty = models.IntegerField()

    def __str__(self):
        return self.user.fname

class Wishlist(models.Model):

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    gold_jew = models.ForeignKey(Gold_jewelry,on_delete=models.CASCADE,null=True)
    dia_jew = models.ForeignKey(Diamond_jewelry,on_delete=models.CASCADE,null=True)
    pt_jew = models.ForeignKey(Platinum_jewelry,on_delete=models.CASCADE,null=True)
    added_date = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.fname

class Transaction(models.Model):

    made_by = models.ForeignKey(User, related_name='transactions', on_delete=models.CASCADE,null=True, blank=True)
    made_on = models.DateTimeField(auto_now_add=True)
    amount = models.IntegerField()
    order_id = models.CharField(unique=True, max_length=100, null=True, blank=True)
    checksum = models.CharField(max_length=100, null=True, blank=True)

    def save(self, *args, **kwargs):
        if self.order_id is None and self.made_on and self.id:
            self.order_id = self.made_on.strftime('PAY2ME%Y%m%dODR') + str(self.id)
        return super().save(*args, **kwargs)