from rest_framework.test import APITestCase
from rest_framework import status
from library.models import User, Book, BookEdition, Review

class ReviewTests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='member', password='password')
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

    def test_create_review(self):
        review = Review.objects.create(
            book=self.book,
            reviewer=self.user,
            review_text="Great book!",
            rating=5
        )
        self.assertEqual(Review.objects.count(), 1)
