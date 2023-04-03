import debug_toolbar
from django.urls import path, include
from rest_framework import routers

from presentation.views import BookList, BookAnnotateView, BookAggregateView, BookSelectRelatedView, \
    BookPrefetchRelatedView, BookDeferView, BookOnlyView, BookRawView, BookExtraView

router = routers.DefaultRouter()
router.register(r'presentation', BookList, basename='presentation')

urlpatterns = [
    path('__debug__/', include(debug_toolbar.urls)),
    path('books/', BookList.as_view()),
    path('books/annotate/', BookAnnotateView.as_view()),
    path('books/aggregate/', BookAggregateView.as_view()),
    path('books/select_related/', BookSelectRelatedView.as_view()),
    path('books/prefetch_related/', BookPrefetchRelatedView.as_view()),
    path('books/defer/', BookDeferView.as_view()),
    path('books/only/', BookOnlyView.as_view()),
    path('books/raw/', BookRawView.as_view()),
    path('books/extra/', BookExtraView.as_view()),

]
