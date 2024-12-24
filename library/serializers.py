from rest_framework import serializers
from .models import User, Book, BookEdition, LoanRecord, Review
from datetime import date

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']

class BookSerializer(serializers.ModelSerializer):
    borrow_count = serializers.IntegerField(read_only=True)  # Otomatik olarak hesaplanır

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date', 'isbn', 'genre', 'stock_count', 'borrow_count']


class BookEditionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookEdition
        fields = ['id', 'book', 'edition_number', 'publication_year', 'format']

from rest_framework import serializers
from datetime import date
from library.models import LoanRecord

class LoanRecordSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanRecord
        fields = ['id', 'member', 'book_edition', 'loan_date', 'return_date']
        read_only_fields = ['loan_date']  # 'loan_date' otomatik olarak ayarlanır

    def validate(self, data):
        # Sadece 'create' işlemi sırasında 'member' doğrulaması yap
        if self.instance is None:
            member = data.get('member')
            if not member:
                raise serializers.ValidationError({"member": "Üye bilgisi gereklidir."})

            # Ödünç alınabilecek maksimum kitap sayısını kontrol et
            active_loans = LoanRecord.objects.filter(member=member, return_date__isnull=True).count()
            if active_loans >= 5:
                raise serializers.ValidationError("Bir üye aynı anda en fazla 5 kitap ödünç alabilir.")

            # Gecikmiş kitap kontrolü
            today = date.today()
            overdue_books = LoanRecord.objects.filter(member=member, return_date__isnull=True, loan_date__lt=today)
            if overdue_books.exists():
                raise serializers.ValidationError("Gecikmiş kitaplar varken yeni bir kitap ödünç alınamaz.")

        return data

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'book', 'reviewer', 'review_text', 'rating', 'created_at']
        read_only_fields = ['reviewer', 'created_at']

    def validate(self, data):
        reviewer = self.context['request'].user
        book = data['book']

        # Ödünç kaydını kontrol et
        active_loans = LoanRecord.objects.filter(
            member=reviewer,
            book_edition__book=book
        )

        print("Reviewer:", reviewer)
        print("Book:", book)
        print("Active Loans QuerySet:", active_loans)
        print("SQL Query:", active_loans.query)

        if not active_loans.exists():
            raise serializers.ValidationError("Bu kitap için inceleme yapabilmek için kitabı ödünç almanız gerekir.")

        return data
