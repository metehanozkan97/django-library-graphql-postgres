from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK
from .models import User, Book, BookEdition, LoanRecord, Review
from .serializers import UserSerializer, BookSerializer, BookEditionSerializer, LoanRecordSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly, IsAdminOrMember, IsMemberOnly
from django.utils.timezone import now
from django.db.models import Count


class CustomPagination(PageNumberPagination):
    page_size = 5  # Her sayfada 5 öğe göster
    page_size_query_param = 'page_size'
    max_page_size = 50


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'user'


class BookViewSet(ModelViewSet):
    print("BookViewSet")
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'book'
    pagination_class = CustomPagination  # Sayfalama sınıfı eklendi
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrReadOnly])
    def increase_stock(self, request, pk=None):
        """Kitap stok sayısını artırır"""
        book = self.get_object()
        increment = request.data.get('increment', 1)  # Artış miktarı
        if not isinstance(increment, int) or increment < 1:
            return Response({"error": "Geçerli bir artış miktarı girin."}, status=400)

        book.stock_count += increment
        book.save()
        return Response({"message": f"Stok {increment} kadar artırıldı.", "new_stock_count": book.stock_count})


class BookSearchView(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ['title', 'author', 'genre', 'isbn']  # Aranabilir alanlar
    ordering_fields = ['title', 'publication_date', 'stock_count']  # Sıralanabilir alanlar
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'search'
    pagination_class = CustomPagination  # Sayfalama sınıfı eklendi


class BookEditionViewSet(viewsets.ModelViewSet):
    queryset = BookEdition.objects.all()
    serializer_class = BookEditionSerializer
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'book_edition'
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdminOrReadOnly])
    def increase_stock(self, request, pk=None):
        """Kitap baskısı stok sayısını artırır"""
        book_edition = self.get_object()
        increment = request.data.get('increment', 1)  # Artış miktarı
        if not isinstance(increment, int) or increment < 1:
            return Response({"error": "Geçerli bir artış miktarı girin."}, status=400)

        book_edition.stock_count += increment
        book_edition.save()
        return Response({"message": f"Stok {increment} kadar artırıldı.", "new_stock_count": book_edition.stock_count})


class LoanRecordViewSet(viewsets.ModelViewSet):
    queryset = LoanRecord.objects.all()
    serializer_class = LoanRecordSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrMember]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'loan_record'

    def create(self, request, *args, **kwargs):
        print("Gelen veri:", request.data)  # Gelen isteği logla
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():  # Doğrulama hatalarını kontrol et
            print("Hatalar:", serializer.errors)  # Hataları logla
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Stok kontrolü
        book_edition = serializer.validated_data['book_edition']
        if book_edition.stock_count <= 0:
            return Response({"error": "Bu kitap stoğu tükenmiş durumda."}, status=status.HTTP_400_BAD_REQUEST)

        # Ödünç alma işlemini kaydet
        book_edition.stock_count -= 1
        book_edition.save()
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        if 'return_date' in request.data:
            # Kitap iade işlemi
            book_edition = instance.book_edition
            book_edition.stock_count += 1
            book_edition.save()
        return super().update(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMember]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review'

    def perform_create(self, serializer):
        print(f"Oturum açmış kullanıcı: {self.request.user}")
        serializer.save(reviewer=self.request.user)

class OverdueLoanRecordsView(APIView):
    print("OverdueLoanRecordsView")
    """
    API Endpoint to list overdue loan records.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Gecikmiş ödünç kayıtlarını al
        overdue_loans = LoanRecord.objects.filter(return_date__isnull=True, loan_date__lt=now())
        print("Overdue Loans:", overdue_loans)
        if not overdue_loans.exists():
            return Response({"message": "Gecikmiş ödünç kaydı bulunmamaktadır."}, status=HTTP_204_NO_CONTENT)
        serializer = LoanRecordSerializer(overdue_loans, many=True)
        return Response(serializer.data, status=HTTP_200_OK)

class MostBorrowedBooksView(APIView):
    """
    En çok ödünç alınan kitapları listeleyen API.
    """
    permission_classes = [IsAuthenticated]  # Giriş yapılmasını zorunlu tutuyoruz

    def get(self, request, *args, **kwargs):
        # En çok ödünç alınan kitapları bul
        books = Book.objects.annotate(
            borrow_count=Count('editions__loanrecord')  # editions -> loanrecord ilişkisini sayar
        ).order_by('-borrow_count')[:5]  # İlk 5 kitabı al
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)
