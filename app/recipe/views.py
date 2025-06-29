"""
Views for the recipe API
"""
from rest_framework import viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Recipe
from recipe import serializers

class RecipeViewSet(viewsets.ModelViewSet):
    """View for manage recipe APIs"""
    serializer_class = serializers.RecipeDetailSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    queryset = Recipe.objects.all()

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by("-id")
    
    def get_serializer_class(self):
        if self.action == "list":
            return serializers.RecipeSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        """Create a new recipe"""
        serializer.save(user=self.request.user)
        
