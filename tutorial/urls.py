import debug_toolbar
from django.urls import path, include
from rest_framework import routers

from presentation.views import BookList, BookAnnotateView, BookAggregateView, \
    BookSelectRelatedView, \
    BookPrefetchRelatedView, BookDeferView, BookOnlyView, BookRawView, BookExtraView, \
    UpdateBookPricesView, \
    FilteredBookListView, CachedBookList, FragmentCachedBookList, PaginatorBooksView, \
    PaginationBasedOnTemplate, LimitOffsetPaginationView, CustomLimitOffsetPaginationView, OneToOneRelationView, \
    ManyToManyRelationView

router = routers.DefaultRouter()
router.register(r'presentation', BookList, basename='presentation')

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('books/<int:pk>/', BookList.as_view()),
    path('books/annotate/', BookAnnotateView.as_view()),
    path('books/aggregate/', BookAggregateView.as_view()),
    path('books/select_related/', BookSelectRelatedView.as_view()),
    path('books/prefetch_related/', BookPrefetchRelatedView.as_view()),
    path('books/defer/', BookDeferView.as_view()),
    path('books/only/', BookOnlyView.as_view()),
    path('books/raw/', BookRawView.as_view()),
    path('books/extra/', BookExtraView.as_view()),
    path('update_prices_with_f_objects/', UpdateBookPricesView.as_view()),
    path('filtered_book_list/', FilteredBookListView.as_view()),
    path('books/with_cache', CachedBookList.as_view()),
    path('books/fragment_cached_book_list', FragmentCachedBookList.as_view()),
    path('books/list_with_paginator', PaginatorBooksView.as_view()),
    path('books/pagination_based_on_template', PaginationBasedOnTemplate.as_view()),
    path('books/limitoffset_pagination_view', LimitOffsetPaginationView.as_view()),
    path('books/custom_limitoffset_pagination_view', CustomLimitOffsetPaginationView.as_view()),
    path('author/one_to_one_relation', OneToOneRelationView.as_view()),
    path('books/many_to_many_relation', ManyToManyRelationView.as_view()),
]
