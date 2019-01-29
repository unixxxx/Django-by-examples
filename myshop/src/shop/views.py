from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin
from .models import (
    Category,
    Product
)


class CategoryMixin(ContextMixin):
    @property
    def category(self):
        category_slug = self.kwargs.get('category_slug', None)
        category = None
        if category_slug:
            category = get_object_or_404(Category, slug=category_slug)
        return category

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductListView(CategoryMixin, ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True)
    extra_context = {
        'categories': Category.objects.all()
    }

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        if self.category:
            queryset = queryset.filter(category=self.category)
        return queryset


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
    query_pk_and_slug = True

    def get_queryset(self):
        queryset = super(ProductDetailView, self).get_queryset()
        queryset = queryset.filter(available=True)
        return queryset
