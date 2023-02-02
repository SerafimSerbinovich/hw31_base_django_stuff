import json

from ads.serializers import *
from django.http import JsonResponse
from django.utils.decorators import method_decorator


from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, ListView, CreateView, DeleteView, UpdateView
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet


class AdPagination(PageNumberPagination):
    page_size = 5


def index(request):
    return JsonResponse({
        "status": "ok"
    }, status=200)


class AdViewSet(ModelViewSet):
    queryset = Ad.objects.order_by('-price')
    default_serializer = AdSerializer
    serializer_classes = {
        'retrieve': AdDetailSerializer,
        'list': AdListSerializer
    }
    pagination_class = AdPagination

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action, self.default_serializer)

    def list(self, request, *args, **kwargs):
        categories = request.GET.getlist('cat')
        if categories:
            self.queryset = self.queryset.filter(category_id__in=categories)

        text = request.GET.get('text')
        if text:
            self.queryset = self.queryset.filter(name__icontains=text)

        location = request.GET.get('location')
        if location:
            self.queryset = self.queryset.filter(author__location__name__icontains=location)

        price_from = request.GET.get('price_from')
        price_to = request.GET.get('price_to')
        if price_from:
            self.queryset = self.queryset.filter(price__gte=price_from)
        if price_to:
            self.queryset = self.queryset.filter(price__lte=price_to)

        return super().list(request, *args, **kwargs)


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


@method_decorator(csrf_exempt, name='dispatch')
class AdImageUpload(UpdateView):
    model = Ad
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.image = request.FILES.get('image')
        self.object.save()
        return JsonResponse({'name': self.object.name, 'image': self.object.image.url})
