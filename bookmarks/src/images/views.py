from django.core.paginator import Paginator, EmptyPage, \
    PageNotAnInteger
from django.http import HttpResponse
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.shortcuts import render
from django.views.generic import View, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import ImageCreateForm
from .models import Image
from .mixins import AjaxRequiredMixin


class ImageCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ImageCreateForm(data=request.GET)
        context = {'section': 'images', 'form': form}
        return render(request, 'images/image/create.html', context)

    def post(self, request):
        form = ImageCreateForm(data=request.POST)
        if form.is_valid():
            # form data is valid
            cd = form.cleaned_data
            new_item = form.save(commit=False)

            # assign current user to the item
            new_item.user = request.user
            new_item.save()
            messages.success(request, 'Image added successfully')

            # redirect to new created item detail view
            return redirect(new_item.get_absolute_url())


class ImageDetailView(LoginRequiredMixin, DetailView):
    model = Image
    template_name = 'images/image/detail.html'


class ImageLikeView(LoginRequiredMixin, AjaxRequiredMixin, View):
    def post(self, request):
        image_id = request.POST.get('id')
        action = request.POST.get('action')
        if image_id and action:
            try:
                image = Image.objects.get(id=image_id)
                if action == 'like':
                    image.users_like.add(request.user)
                else:
                    image.users_like.remove(request.user)
                return JsonResponse({'status': 'ok'})
            except:
                pass
        return JsonResponse({'status': 'ko'})


@login_required
def image_list(request):
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer deliver the first page
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            # If the request is AJAX and the page is out of range
            # return an empty page
            return HttpResponse('')
        # If page is out of range deliver last page of results
        images = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request,
                      'images/image/list_ajax.html',
                      {'section': 'images', 'images': images})
    return render(request,
                  'images/image/list.html',
                  {'section': 'images', 'images': images})
