from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import ContextMixin
from cart.forms import CartAddProductForm
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
            language = self.request.LANGUAGE_CODE
            print(language)
            category = get_object_or_404(Category,
                                         translations__language_code=language,
                                         translations__slug=category_slug)
        return category

    def get_context_data(self, **kwargs):
        context = super(CategoryMixin, self).get_context_data(**kwargs)
        context['category'] = self.category
        return context


class ProductListView(CategoryMixin, ListView):
    template_name = 'shop/product/list.html'
    context_object_name = 'products'
    queryset = Product.objects.filter(available=True)

    def get_queryset(self):
        queryset = super(ProductListView, self).get_queryset()
        if self.category:
            queryset = queryset.filter(category=self.category)
        return queryset

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'shop/product/detail.html'
    context_object_name = 'product'
    query_pk_and_slug = True
    extra_context = {
        'cart_product_form': CartAddProductForm()
    }

    def get_object(self):
        language = self.request.LANGUAGE_CODE
        id = self.kwargs['id']
        slug = self.kwargs['slug']
        product = get_object_or_404(self.model,
                                    id=id,
                                    translations__language_code=language,
                                    translations__slug=slug,
                                    available=True)
        return product
