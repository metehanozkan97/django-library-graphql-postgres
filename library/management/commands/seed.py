from django.core.management.base import BaseCommand
from library.models import Book, BookEdition, LoanRecord
from django.contrib.auth import get_user_model

User = get_user_model()  # Özel kullanıcı modelini alın


class Command(BaseCommand):
    help = 'Seed the database with example data'

    def handle(self, *args, **kwargs):
        # Kullanıcılar
        if not User.objects.filter(username='testuser').exists():
            user1 = User.objects.create_user(username='testuser', password='password', role='member')
            user1.save()
            self.stdout.write(self.style.SUCCESS('User created: testuser'))
        else:
            user1 = User.objects.get(username='testuser')

        if not User.objects.filter(username='username').exists():
            user2 = User.objects.create_superuser(username='username', password='password', role='admin')
            user2.is_staff = True
            user2.is_superuser = True
            user2.save()
            self.stdout.write(self.style.SUCCESS('Superuser created: username'))
        else:
            user2 = User.objects.get(username='username')

        # Kitaplar
        if not Book.objects.filter(title='Django ile Web Geliştirme').exists():
            book1 = Book.objects.create(
                title='Django ile Web Geliştirme',
                author='Ahmet Yılmaz',
                publication_date='2023-01-01',
                isbn='9781234567890',
                genre='Programming',
                stock_count=10
            )
            self.stdout.write(self.style.SUCCESS(f'Book created: {book1.title}'))
        else:
            book1 = Book.objects.get(title='Django ile Web Geliştirme')

        if not Book.objects.filter(title='Python ile Veri Bilimi').exists():
            book2 = Book.objects.create(
                title='Python ile Veri Bilimi',
                author='Mehmet Kaya',
                publication_date='2022-05-15',
                isbn='9789876543210',
                genre='Data Science',
                stock_count=15
            )
            self.stdout.write(self.style.SUCCESS(f'Book created: {book2.title}'))
        else:
            book2 = Book.objects.get(title='Python ile Veri Bilimi')

        # Kitap Baskıları
        if book1 and not BookEdition.objects.filter(book=book1).exists():
            edition1 = BookEdition.objects.create(
                book=book1,
                edition_number=1,
                publication_year=2023,
                format='hardcover',
                stock_count=5
            )
            self.stdout.write(self.style.SUCCESS(f'Book Edition created: {edition1}'))
        else:
            edition1 = BookEdition.objects.filter(book=book1).first()

        if book2 and not BookEdition.objects.filter(book=book2).exists():
            edition2 = BookEdition.objects.create(
                book=book2,
                edition_number=2,
                publication_year=2023,
                format='paperback',
                stock_count=7
            )
            self.stdout.write(self.style.SUCCESS(f'Book Edition created: {edition2}'))
        else:
            edition2 = BookEdition.objects.filter(book=book2).first()

        # Ödünç Kayıtları
        if edition1 and not LoanRecord.objects.filter(member=user1).exists():
            loan1 = LoanRecord.objects.create(
                member=user1,
                book_edition=edition1,
                loan_date='2024-12-23'
            )
            self.stdout.write(self.style.SUCCESS(f'Loan Record created for user: {user1.username}'))

        if edition2 and not LoanRecord.objects.filter(member=user2).exists():
            loan2 = LoanRecord.objects.create(
                member=user2,
                book_edition=edition2,
                loan_date='2024-12-23'
            )
            self.stdout.write(self.style.SUCCESS(f'Loan Record created for user: {user2.username}'))

        self.stdout.write(self.style.SUCCESS('Seeding completed successfully!'))
