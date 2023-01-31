import json

from django.db.models import Count, Q
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from users.models import User, Location


class UserDetailView(DetailView):
    model = User

    def get(self, request, *args, **kwargs):
        try:
            user = self.get_object()
        except User.DoesNotExist:
            return JsonResponse({'error': 'Not found'}, status=404)

        return JsonResponse({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'role': user.role,
            'age': user.age,
            'location': [location.name for location in user.location.all()]
        })


class UserListView(ListView):
    model = User
    queryset = User.objects.annotate(total_ads=Count('ad', filter=Q(ad__is_published=True)))

    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)

        return JsonResponse([{
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'username': user.username,
            'role': user.role,
            'age': user.age,
            'total_ads': user.total_ads,
            'location': [location.name for location in user.location.all()]
        } for user in self.object_list], safe=False)


@method_decorator(csrf_exempt, name='dispatch')
class UserCreateView(CreateView):
    model = User
    fields = '__all__'

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)

        new_user = User.objects.create(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            username=data.get('username'),
            password=data.get('password'),
            role=data.get('role'),
            age=data.get('age'))

        locations = data.get('location')

        if locations:
            for location_name in locations:
                loc, created = Location.objects.get_or_create(name=location_name)
                new_user.location.add(loc)

        return JsonResponse({
            'id': new_user.id,
            'first_name': new_user.first_name,
            'last_name': new_user.last_name,
            'username': new_user.username,
            'role': new_user.role,
            'age': new_user.age,
            'location': [location.name for location in new_user.location.all()]
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserUpdateView(UpdateView):
    model = User
    fields = '__all__'

    def patch(self, request, *args, **kwargs):
        super().post(request, *args, **kwargs)
        data = json.loads(request.body)

        if 'first_name' in data:
            self.object.first_name = data['first_name']
        if 'last_name' in data:
            self.object.last_name = data['last_name']
        if 'username' in data:
            self.object.username = data['username']

        if 'location' in data:
            self.object.location.all().delete()
            for location_name in data['location']:
                loc, created = Location.objects.get_or_create(name=location_name)
                self.object.location.add(loc)

        return JsonResponse({
            'id': self.object.id,
            'first_name': self.object.first_name,
            'last_name': self.object.last_name,
            'username': self.object.username,
            'role': self.object.role,
            'age': self.object.age,
            'location': [location.name for location in self.object.location.all()]
        })


@method_decorator(csrf_exempt, name='dispatch')
class UserDeleteView(DeleteView):
    model = User
    success_url = '/'

    def delete(self, request, *args, **kwargs):
        user = self.get_object()
        super().delete(request, *args, **kwargs)
        return JsonResponse({'id': user.id})
