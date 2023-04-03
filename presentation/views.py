from rest_framework import generics
from .models import Book, Author
from .serializers import BookSerializer, AuthorSerializer, OnlyBookSerializer
from django.db.models.functions import Length
from rest_framework.response import Response
from django.db.models import Avg, Count


class BookList(generics.ListCreateAPIView):
    # Queryset
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class BookAnnotateView(generics.ListCreateAPIView):
    # Queryset with annotation
    queryset = Book.objects.annotate(
        title_length=Length('title')
    )
    serializer_class = BookSerializer


class BookAggregateView(generics.GenericAPIView):
    # Queryset with aggregation
    queryset = Book.objects.all()

    def get(self, request, *args, **kwargs):
        aggregate_data = self.queryset.aggregate(average_price=Avg('price'), total_books=Count('id'))
        return Response(aggregate_data)


class BookSelectRelatedView(generics.ListAPIView):
    # Queryset with annotation and select_related
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.select_related('author').annotate(title_length=Length('title'))


class BookPrefetchRelatedView(generics.ListAPIView):
    # Queryset with prefetch_related
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.prefetch_related('book_set')


class BookDeferView(generics.ListAPIView):
    # Queryset with Defer
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.defer('publication_date').annotate(title_length=Length('title'))


class BookOnlyView(generics.ListAPIView):
    # Queryset with Only
    serializer_class = OnlyBookSerializer

    def get_queryset(self):
        return Book.objects.only('title', 'price')


class BookRawView(generics.ListAPIView):
    # Queryset with RAW
    serializer_class = OnlyBookSerializer

    def get_queryset(self):
        raw_sql = 'SELECT title, price FROM presentation_book'
        return Book.objects.raw(raw_sql)


class BookExtraView(generics.ListAPIView):
    # Queryset with Extra
    serializer_class = OnlyBookSerializer

    def get_queryset(self):
        return Book.objects.extra(select={'title': 'title', 'price': 'price'})
