from rest_framework.test import APITestCase
from rest_framework import status
from library.models import Book, BookEdition, User

class BookEditionTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword', role='admin')
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            publication_date="2024-01-01",
            isbn="1234567890123",
            genre="Fiction",
            stock_count=10
        )
        self.book_edition = BookEdition.objects.create(
            book=self.book,
            edition_number=1,
            publication_year=2024,
            format="hardcover",
            stock_count=5
        )

    def authenticate(self):
        response = self.client.post('/api/token/', {'username': 'testuser', 'password': 'testpassword'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')

    def test_get_book_editions(self):
        self.authenticate()  # Kimlik doğrulama ekledik
        response = self.client.get('/api/book-editions/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
