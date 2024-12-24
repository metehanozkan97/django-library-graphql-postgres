from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from library.models import Book, BookEdition

User = get_user_model()

class BaseTestCase(APITestCase):
    def setUp(self):
        """Ortak test setup işlemleri"""
        # Admin kullanıcı oluştur
        self.admin_user = User.objects.create_superuser(
            username='adminuser',
            password='adminpassword',
            role=User.Roles.ADMIN
        )
        # Üye kullanıcı oluştur
        self.member_user = User.objects.create_user(
            username='testuser',
            password='testpassword',
            role=User.Roles.MEMBER
        )
        # Ortak bir kitap oluştur
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date="2024-01-01",
            isbn="1234567890123",
            genre="Fiction",
            stock_count=10
        )
        # Ortak bir kitap baskısı oluştur
        self.book_edition = BookEdition.objects.create(
            book=self.book,
            edition_number=1,
            publication_year=2024,
            format="hardcover",
            stock_count=5
        )

    def authenticate_as_admin(self):
        """Admin kullanıcı olarak kimlik doğrulama"""
        self.client.force_authenticate(user=self.admin_user)

    def authenticate_as_member(self):
        """Üye kullanıcı olarak kimlik doğrulama"""
        self.client.force_authenticate(user=self.member_user)
