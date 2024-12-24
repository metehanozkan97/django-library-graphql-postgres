from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """
    Sadece admin kullanıcılar için tam erişim, diğer kullanıcılar için yalnızca okunabilir izin.
    """
    def has_permission(self, request, view):
        # Güvenli yöntemler (GET, HEAD, OPTIONS) için izin verilir
        if request.method in SAFE_METHODS:
            return True
        # Admin kullanıcılar için tam izin
        return request.user.is_authenticated and request.user.role == 'admin'


class IsAdminOrMember(BasePermission):
    """
    Admin kullanıcılar için tam erişim, üyeler için sınırlı erişim.
    """
    def has_permission(self, request, view):
        # Admin kullanıcılar her şeye erişebilir
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        # Üyeler yalnızca listeleme ve kendi incelemelerini ekleyebilir
        if request.method in ['GET', 'POST']:
            return request.user.is_authenticated and request.user.role == 'member'
        return False

    def has_object_permission(self, request, view, obj):
        # Admin kullanıcılar her şeye erişebilir
        if request.user.is_authenticated and request.user.role == 'admin':
            return True
        # Üyeler yalnızca kendi nesnelerini düzenleyebilir veya silebilir
        if request.user.is_authenticated and request.user.role == 'member':
            return obj.reviewer == request.user  # Örneğin Review modeli için
        return False


class IsMemberOnly(BasePermission):
    """
    Üyelerin kitap ödünç almasına izin verir, diğer rollere kısıtlama getirir.
    """
    def has_permission(self, request, view):
        # Sadece üye rolündeki kullanıcılar için izin
        return request.user.is_authenticated and request.user.role == 'member'

    def has_object_permission(self, request, view, obj):
        # Üyeler yalnızca kendi nesnelerine erişebilir
        return request.user.is_authenticated and obj.member == request.user
