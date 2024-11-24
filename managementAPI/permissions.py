from rest_framework.permissions import BasePermission,IsAuthenticated,IsAdminUser

'''
creating custom permissions for admin role only
'''
class IsAdminRole(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role=="ADMIN":
            return True
        return bool(request.user and request.user.is_staff)
    

'''
creating custom permissions for user role only
'''
class AuthenticateUserOnly(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated and request.user.role=="USER":
            return True
        return bool(request.user and request.user.is_staff)
    
