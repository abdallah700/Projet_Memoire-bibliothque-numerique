
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse

from datetime import timedelta


#User = get_user_model()


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_publisher = models.BooleanField(default=False)
    is_librarian = models.BooleanField(default=False)
    is_student = models.BooleanField(default=False)

    class Meta:
        swappable = 'AUTH_USER_MODEL'


class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    year = models.CharField(max_length=100)
    nbr_exemplaire = models.IntegerField(null=True, blank=True)
    cote_book = models.CharField(max_length=200, null=True, blank=True)
    num_invetaire = models.CharField(max_length=200, null=True, blank=True)
    publisher = models.CharField(max_length=200)
    desc = models.CharField(max_length=1000)
    uploaded_by = models.CharField(max_length=100, null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    pdf = models.FileField(upload_to='bookapp/pdfs/')
    cover = models.ImageField(upload_to='bookapp/covers/', null=True, blank=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        self.pdf.delete()
        self.cover.delete()
        super().delete(*args, **kwargs)


class Reservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now=True, null=True)
    expiration_date = models.DateTimeField(null=True, blank=True)
    canceled = models.BooleanField(default=False)  # Champ pour indiquer si la réservation a été annulée

    def __str__(self):
        return str(self.added_at)

    def get_absolute_url(self):
        return reverse('reservation_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"Reservation {self.id} by {self.user.username} for {self.book.title}"

    def save(self, *args, **kwargs):
        if not self.expiration_date:
            self.expiration_date = timezone.now() + timedelta(minutes=30)
        super().save(*args, **kwargs)



class CancelledReservation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    added_at = models.DateTimeField()
    cancelled_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.book} - {self.cancelled_at}"




class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    posted_at = models.DateTimeField(auto_now=True, null=True)


    def __str__(self):
        return str(self.message)



class DeleteRequest(models.Model):
    delete_request = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.delete_request


class Feedback(models.Model):
    feedback = models.CharField(max_length=100, null=True, blank=True)


    def __str__(self):
        return self.feedback












