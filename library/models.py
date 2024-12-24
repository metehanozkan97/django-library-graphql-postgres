from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

# Custom User model with roles
class User(AbstractUser):
    class Roles(models.TextChoices):
        ADMIN = 'admin', _('Admin')
        MEMBER = 'member', _('Member')

    role = models.CharField(
        max_length=10,
        choices=Roles.choices,
        default=Roles.MEMBER,
    )

    @property
    def is_admin(self):
        return self.role == self.Roles.ADMIN

    @property
    def is_member(self):
        return self.role == self.Roles.MEMBER

# Book model
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    publication_date = models.DateField()
    isbn = models.CharField(max_length=13, unique=True)
    genre = models.CharField(max_length=100)
    stock_count = models.PositiveIntegerField()

    class Meta:
        ordering = ['title']

    def __str__(self):
        return self.title

# Book Edition model
class BookEdition(models.Model):
    FORMAT_CHOICES = [
        ('hardcover', 'Hardcover'),
        ('paperback', 'Paperback'),
        ('ebook', 'eBook'),
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='editions')
    edition_number = models.PositiveIntegerField()
    publication_year = models.PositiveIntegerField()
    format = models.CharField(max_length=20, choices=FORMAT_CHOICES)
    stock_count = models.PositiveIntegerField(default=0) 

    class Meta:
        ordering = ['edition_number']

    def __str__(self):
        return f"{self.book.title} - Edition {self.edition_number}"

# Loan Record model
class LoanRecord(models.Model):
    member = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'member'})
    book_edition = models.ForeignKey(BookEdition, on_delete=models.CASCADE)
    loan_date = models.DateField(auto_now_add=True)  # Otomatik olarak bugünün tarihini ayarlar
    return_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.member.username} borrowed {self.book_edition.book.title}"

# Review model
class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'member'})
    review_text = models.TextField()
    rating = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review by {self.reviewer.username} for {self.book.title}"
