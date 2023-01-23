from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.
class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = PhoneNumberField(help_text='Contact Phone Number', unique=True)


    USERNAME_FIELD = ('email')
    REQUIRED_FIELDS = ['first_name', 'last_name', 'username', 'phone_number']

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name} {self.username}'


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    current_balance = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(0)])
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'Account for {self.user.first_name} {self.user.last_name} with account balance of {self.current_balance}'

PAYMENT_METHODS_CHOICES = (
    ('M-Pesa', 'M-Pesa'),
    ('Credit-Card', 'Credit-Card')
)


TRANSACTION_TYPE_CHOICES = (
    ('Send', 'Send'),
    ('Receive', 'Receive')
)

class Transactions(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    amount = models.DecimalField(max_digits=9, decimal_places=2, validators=[MinValueValidator(1)])
    payment_method = models.CharField(max_length=100, choices=PAYMENT_METHODS_CHOICES)
    done_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'Transaction by {self.sender.username} to {self.receiver.username}'