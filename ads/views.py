import json

from ads.models import Ad, Category
from django.http import JsonResponse
from django.utils.decorators import method_decorator

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView


def index(request):
    return JsonResponse({
        "status": "ok"
    }, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class AdsView(View):
    def get(self, request):
        all_ads = Ad.objects.all()

        response = []

        for ad in all_ads:
            response.append({
                'id': ad.id,
                'name': ad.name,
                'author': ad.author,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published,
                'price': ad.price
            })
        return JsonResponse(response, safe=False,)

    def post(self, request):
        ad_data = json.loads(request.body)

        ad = Ad.objects.create(
            name=ad_data['name'],
            author=ad_data['author'],
            description=ad_data['description'],
            address=ad_data['address'],
            is_published=ad_data['is_published'],
            price=ad_data['price']
        )

        return JsonResponse({
            'id': ad.id,
            'name': ad.name

        })


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
                'author': ad.author,
                'description': ad.description,
                'address': ad.address,
                'is_published': ad.is_published,
                'price': ad.price
            })


@method_decorator(csrf_exempt, name='dispatch')
class CategoriesView(View):
    def get(self, request):
        all_categories = Category.objects.all()

        response = []
        for category in all_categories:
            response.append({
                'id': category.id,
                'name': category.name
            })

        return JsonResponse(response, safe=False)

    def post(self, request):
        category_data = json.loads(request.body)

        category = Category.objects.create(
            name=category_data['name']
        )

        return JsonResponse({
            'id': category.id,
            'name': category.name
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
