from rest_framework.permissions import BasePermission
from users.models import User


class IsSelectionOwner(BasePermission):
    message = 'Вы не имеете права изменять эту подборку'

    def has_object_permission(self, request, view, selection):
        if request.user == selection.owner:
            return True
        return False


class IsAdAuthorOrStaff(BasePermission):
    message = 'Только админ или владелец может изменять это объявление'

    def has_object_permission(self, request, view, ad):
        if request.user == ad.author or request.user != User.CHOICES[0][0]:
            return True
        return False
