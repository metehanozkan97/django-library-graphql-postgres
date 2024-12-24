import graphene
from graphene_django.types import DjangoObjectType
from graphene_django.filter import DjangoFilterConnectionField, GlobalIDFilter
from graphene_django.filter.utils import get_filtering_args_from_filterset
from library.models import Book, BookEdition, LoanRecord, Review, User
import django_filters

# User Type
class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role']
        interfaces = (graphene.relay.Node,)

# Book FilterSet
class BookFilter(django_filters.FilterSet):
    class Meta:
        model = Book
        fields = {
            'title': ['exact', 'icontains', 'istartswith'],
            'author': ['exact', 'icontains'],
            'genre': ['exact', 'icontains'],
            'publication_date': ['exact', 'year__gt', 'year__lt'],
        }

# BookEdition FilterSet
class BookEditionFilter(django_filters.FilterSet):
    class Meta:
        model = BookEdition
        fields = {
            'edition_number': ['exact', 'gte', 'lte'],
            'publication_year': ['exact', 'gte', 'lte'],
            'format': ['exact', 'icontains'],
        }

# LoanRecord FilterSet
class LoanRecordFilter(django_filters.FilterSet):
    class Meta:
        model = LoanRecord
        fields = {
            'loan_date': ['exact', 'gte', 'lte'],
            'return_date': ['exact', 'gte', 'lte'],
            'member': ['exact'],
            'book_edition': ['exact'],
        }

# Review FilterSet
class ReviewFilter(django_filters.FilterSet):
    reviewer = GlobalIDFilter()

    class Meta:
        model = Review
        fields = {
            'rating': ['exact', 'gte', 'lte'],
            'reviewer': ['exact'],
            'book': ['exact'],
        }

# Book Type
class BookType(DjangoObjectType):
    class Meta:
        model = Book
        interfaces = (graphene.relay.Node,)

# BookEdition Type
class BookEditionType(DjangoObjectType):
    class Meta:
        model = BookEdition
        interfaces = (graphene.relay.Node,)

# LoanRecord Type
class LoanRecordType(DjangoObjectType):
    class Meta:
        model = LoanRecord
        interfaces = (graphene.relay.Node,)

    member = graphene.Field(UserType)
    book_edition = graphene.Field(BookEditionType)

    def resolve_member(self, info):
        return self.member

    def resolve_book_edition(self, info):
        return self.book_edition

# Review Type
class ReviewType(DjangoObjectType):
    class Meta:
        model = Review
        interfaces = (graphene.relay.Node,)

# Query
class Query(graphene.ObjectType):
    all_books = DjangoFilterConnectionField(BookType, filterset_class=BookFilter)
    all_book_editions = DjangoFilterConnectionField(BookEditionType, filterset_class=BookEditionFilter)
    all_loan_records = DjangoFilterConnectionField(LoanRecordType, filterset_class=LoanRecordFilter)
    all_reviews = DjangoFilterConnectionField(ReviewType, filterset_class=ReviewFilter)
    all_users = graphene.List(UserType)

    book_by_id = graphene.Field(BookType, id=graphene.Int(required=True))
    loan_record_by_id = graphene.Field(LoanRecordType, id=graphene.Int(required=True))

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_book_by_id(self, info, id):
        return Book.objects.get(pk=id)

    def resolve_loan_record_by_id(self, info, id):
        return LoanRecord.objects.get(pk=id)

# Mutasyonlar
class CreateBook(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        author = graphene.String(required=True)
        publication_date = graphene.String(required=True)
        isbn = graphene.String(required=True)
        genre = graphene.String(required=True)
        stock_count = graphene.Int(required=True)

    book = graphene.Field(BookType)

    def mutate(self, info, title, author, publication_date, isbn, genre, stock_count):
        book = Book.objects.create(
            title=title,
            author=author,
            publication_date=publication_date,
            isbn=isbn,
            genre=genre,
            stock_count=stock_count
        )
        return CreateBook(book=book)

class CreateLoanRecord(graphene.Mutation):
    class Arguments:
        member_id = graphene.Int(required=True)
        book_edition_id = graphene.Int(required=True)

    loan_record = graphene.Field(LoanRecordType)

    def mutate(self, info, member_id, book_edition_id):
        book_edition = BookEdition.objects.get(pk=book_edition_id)

        if book_edition.stock_count <= 0:
            raise Exception("Kitap stoğu tükenmiş durumda!")

        loan_record = LoanRecord.objects.create(
            member=info.context.user,
            book_edition=book_edition
        )
        book_edition.stock_count -= 1
        book_edition.save()
        return CreateLoanRecord(loan_record=loan_record)

class Mutation(graphene.ObjectType):
    create_book = CreateBook.Field()
    create_loan_record = CreateLoanRecord.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
