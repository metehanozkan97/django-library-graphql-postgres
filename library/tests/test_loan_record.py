from rest_framework.test import APITestCase
from rest_framework import status
from library.models import User, Book, BookEdition, LoanRecord

class LoanRecordTests(APITestCase):

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

    def test_create_loan_record(self):
        loan = LoanRecord.objects.create(
            member=self.user,
            book_edition=self.book_edition
        )
        self.assertEqual(LoanRecord.objects.count(), 1)
