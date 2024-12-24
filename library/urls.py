from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,
    BookViewSet,
    BookEditionViewSet,
    BookSearchView,
    LoanRecordViewSet,
    OverdueLoanRecordsView,
    ReviewViewSet,
    MostBorrowedBooksView,
)
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from graphene_django.views import GraphQLView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


# Router ile otomatik endpoint oluşturma
router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'books', BookViewSet)
router.register(r'book-editions', BookEditionViewSet)
router.register(r'loan-records', LoanRecordViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = [
    path('', include(router.urls)),  # Tüm router URL'leri
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('books/search/', csrf_exempt(BookSearchView.as_view()), name='book-search'),
    path('loan-records/overdue/', csrf_exempt(OverdueLoanRecordsView.as_view()), name='overdue-loans'),
    path('books/most-borrowed/', csrf_exempt(MostBorrowedBooksView.as_view()), name='most-borrowed-books'),
    path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),  # CSRF doğrulaması kaldırıldı
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
