import debug_toolbar
from django.urls import path, include
from rest_framework import routers

from presentation.views import BookList, BookAnnotateView, BookAggregateView, BookSelectRelatedView, \
    BookPrefetchRelatedView, BooksDeferView, BooksOnlyView

router = routers.DefaultRouter()
router.register(r'presentation', BookList, basename='presentation')

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('books/', BookList.as_view()),
    path('books/annotate/', BookAnnotateView.as_view()),
    path('books/aggregate/', BookAggregateView.as_view()),
    path('books/select_related/', BookSelectRelatedView.as_view()),
    path('books/prefetch_related/', BookPrefetchRelatedView.as_view()),
    path('books/defer/', BooksDeferView.as_view()),
    path('books/only/', BooksOnlyView.as_view()),
]
