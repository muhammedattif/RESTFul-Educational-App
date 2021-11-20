from django.urls import path, include
from categories.api.views import CategoryList, CategoryFilter

app_name = 'categories'

urlpatterns = [
    # Categories APIs
    path('', CategoryList.as_view(), name='categories'),
    path('<int:category_id>', CategoryFilter.as_view(), name='filter_by_category')
]