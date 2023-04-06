from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import generics
from rest_framework.pagination import LimitOffsetPagination

from .models import Book, Author, AuthorProfile, Category, SecondTableBooks
from .serializers import BookSerializer, AuthorSerializer, OnlyBookSerializer, \
    AuthorProfileSerializer, \
    CategorySerializer, Db2BookSerializer
from django.db.models.functions import Length
from rest_framework.response import Response
from django.db.models import Avg, Count
from django.db import connection
from django.db.models import F, Q
from rest_framework import views, status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class BookList(generics.RetrieveAPIView):
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
        aggregate_data = self.queryset.aggregate(average_price=Avg('price'),
                                                 total_books=Count('id'))
        return Response(aggregate_data)


class BookSelectRelatedView(generics.ListAPIView):
    # Queryset with annotation and select_related
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.select_related('author').annotate(
            title_length=Length('title'))


class BookPrefetchRelatedView(generics.ListAPIView):
    # Queryset with prefetch_related
    serializer_class = AuthorSerializer

    def get_queryset(self):
        return Author.objects.prefetch_related('book_set')


class BookDeferView(generics.ListAPIView):
    # Queryset with Defer
    serializer_class = BookSerializer

    def get_queryset(self):
        return Book.objects.defer('publication_date').annotate(
            title_length=Length('title'))


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
        with connection.cursor() as cursor:
            cursor.execute(raw_sql)
            results = cursor.fetchall()
            return [
                Book(title=row[0], price=row[1])
                for row in results
            ]


class BookExtraView(generics.ListAPIView):
    # Queryset with Extra
    serializer_class = OnlyBookSerializer

    def get_queryset(self):
        return Book.objects.extra(select={'title': 'title', 'price': 'price'})


class UpdateBookPricesView(views.APIView):
    # Queryset with F Object
    @staticmethod
    def get(request, *args, **kwargs):
        Book.objects.update(price=F('price') * 1.1)
        return Response({"message": "Book prices updated"}, status=status.HTTP_200_OK)


class FilteredBookListView(generics.ListAPIView):
    # Queryset with Q Object
    serializer_class = BookSerializer

    def get_queryset(self):
        query = self.request.query_params.get('query', '')
        queryset = Book.objects.filter(
            Q(title__icontains=query)
        )
        return queryset


class CachedBookList(generics.ListCreateAPIView):
    # Queryset with catch used MethodDecorator
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @method_decorator(cache_page(60))
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class FragmentCachedBookList(generics.ListCreateAPIView):
    # A query set with a catch function using fragment capture
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        context = {'book_list': queryset}
        return render(request, 'book_list.html', context)


class PaginatorBooksView(generics.ListCreateAPIView):
    def get(self, request, *args, **kwargs):
        queryset = Book.objects.all().order_by('id')
        paginator = Paginator(queryset, 2)
        page = request.GET.get('page')
        items = paginator.get_page(page)

        serializer = BookSerializer(items, many=True)
        serialized_data = serializer.data

        response_data = {
            'results': serialized_data,
            'has_next': items.has_next(),
            'has_previous': items.has_previous(),
            'num_pages': paginator.num_pages,
        }

        return JsonResponse(response_data)


class PaginationBasedOnTemplate(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset().order_by('id')

        paginator = Paginator(queryset, 2)
        page = request.GET.get('page')
        books = paginator.get_page(page)

        context = {'book_list': books}
        return render(request, 'book_list_2.html', context)


class LimitOffsetPaginationView(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = LimitOffsetPagination
    queryset = Book.objects.all()


class CustomLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2


class CustomLimitOffsetPaginationView(generics.ListAPIView):
    serializer_class = BookSerializer
    pagination_class = CustomLimitOffsetPagination
    queryset = Book.objects.all()


class OneToOneRelationView(generics.ListCreateAPIView):
    serializer_class = AuthorProfileSerializer
    queryset = AuthorProfile.objects.all()


class ManyToManyRelationView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class FilteredBooksToDb2(generics.ListAPIView):
    serializer_class = Db2BookSerializer

    def get_queryset(self):
        all_books = Book.objects.all()
        book_serializer = OnlyBookSerializer(all_books, many=True)

        for book_data, original_book in zip(book_serializer.data, all_books):
            if not original_book:
                continue

            new_book = SecondTableBooks()
            new_book.title = book_data['title']
            new_book.price = book_data['price']

            author = original_book.author
            author_serializer = AuthorProfileSerializer(author.authorprofile)

            author_name = author_serializer.data['author']['name']
            new_book.author = author_name

            new_book.save(using='mydatabase')

        return all_books
