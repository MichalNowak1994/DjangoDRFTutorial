from rest_framework import serializers
from .models import Book, Author, AuthorProfile, Category


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name']


class AuthorProfileSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)

    class Meta:
        model = AuthorProfile
        fields = ('author', 'publishing_house', 'date_of_birth')


class OnlyBookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'price']


class BookSerializer(serializers.ModelSerializer):
    title_length = serializers.IntegerField(read_only=True)
    author = AuthorSerializer()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date', 'price', 'title_length']

    def create(self, validated_data):
        author_data = validated_data.pop('author')
        author, created = Author.objects.get_or_create(name=author_data['name'])
        book = Book.objects.create(author=author, **validated_data)
        return book


class CategorySerializer(serializers.ModelSerializer):
    book_set = BookSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'book_set']


class Db2BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price']
