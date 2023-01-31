import json

from ads.models import Ad, Category
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator


from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from users.models import User


def index(request):
    return JsonResponse({
        "status": "ok"
    }, status=200)


class AdDetailView(DetailView):
    model = Ad

    def get(self, request, *args, **kwargs):
        try:
            ad = self.get_object()
        except Ad.DoesNotExist:
            return JsonResponse({'error': 'Not  Found'}, status=404)

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.id,
            'category': ad.category.name,
            'description': ad.description,
            'is_published': ad.is_published,
            'price': ad.price
        })


class CategoryDetailView(DetailView):
    model = Category

    def get(self, request, *args, **kwargs):
        try:
            category = self.get_object()
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse({
            'id': category.id,
            'name': category.name
        })


class CategoryListView(ListView):
    model = Category
    queryset = Category.objects.order_by('name').all()

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return JsonResponse([{
            'id': category.id,
            'name': category.name
        } for category in self.object_list], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def post(self, request, **kwargs):
        data = json.loads(request.body)
        new_category = Category.objects.create(
            name=data.get('name'),
        )
        return JsonResponse({'id': new_category.id, 'name': new_category.name}, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class CategoryUpdateView(UpdateView):
    model = Category
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get('name')
        self.object.save()
        return JsonResponse({'id': self.object.id, 'name': self.object.name})

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)
        self.object.name = data.get('name')
        self.object.save()
        return JsonResponse({'id': self.object.id, 'name': self.object.name})


@method_decorator(csrf_exempt, name='dispatch')
class CategoryDeleteView(DeleteView):
    model = Category
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        category = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({'id': category.id})


class AdListView(ListView):
    model = Ad
    queryset = Ad.objects.order_by('-price').select_related('author')

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        paginator = Paginator(self.object_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return JsonResponse({
            'total': page_obj.paginator.count,
            'num_pages': page_obj.paginator.num_pages,
            'items': [{'id': ad.id,
                       'name': ad.name,
                       'author': ad.author.first_name,
                       'price': ad.price,
                       'description': ad.description,
                       'is_published': ad.is_published,
                       'category_id': ad.category_id,
                       'image': ad.image.url if ad.image else None

                       } for ad in page_obj]
        }, safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class AdCreateView(CreateView):
    model = Ad
    fields = '__all__'

    def post(self, request, **kwargs):
        data = json.loads(request.body)

        author = get_object_or_404(User, username=data.get('username'))
        category = get_object_or_404(Category, name=data.get('category'))
        ad = Ad.objects.create(
            name=data.get('name'),
            author=author,
            price=data.get('price'),
            description=data.get('description'),
            is_published=data.get('is_published'),
            category=category

        )

        return JsonResponse({
            'id': ad.id,
            'name': ad.name,
            'author': ad.author.username,
            'category': ad.category.name,
            'price': ad.price,
            'description': ad.description,
            'is_published': ad.is_published,

        })


@method_decorator(csrf_exempt, name='dispatch')
class AdUpdateView(UpdateView):
    model = Ad
    fields = '__all__'

    def put(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        self.object.name = data.get('name')
        self.object.autor = get_object_or_404(User, username=data.get('username'))
        self.object.category = get_object_or_404(Category, name=data.get('category'))
        self.object.price = data.get('price')
        self.object.is_published = data.get('is_published')
        self.object.description = data.get('description')

        return JsonResponse({
            'id': self.object.id,
            'name': self.object.name,
            'author': self.object.author.first_name,
            'category': self.object.category.id,
            'price': self.object.price,
            'description': self.object.description,
            'is_published': self.object.is_published

        })


@method_decorator(csrf_exempt, name='dispatch')
class AdDeleteView(DeleteView):
    model = Ad
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        ad = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({'id': ad.id})


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpload(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({'name': self.object.name, 'image': self.object.image.url})
