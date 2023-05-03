from rest_framework.permissions import BasePermission

class IsEditorOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            # Permite el acceso a los usuarios autenticados que no pertenecen al grupo 'Editor' solo para el método GET.
            return request.user.is_authenticated and not request.user.groups.filter(name='Editor').exists()
        else:
            # Permite el acceso completo a los usuarios que pertenecen al grupo 'Editor'.
            return request.user.is_authenticated and request.user.groups.filter(name='Editor').exists()