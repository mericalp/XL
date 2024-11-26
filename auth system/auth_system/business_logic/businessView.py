from rest_framework.views import APIView
from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.http import HttpResponse


class EntityView(View):
    model = None
    form_class = None
    template_name = None
    filter_by_user = False
    context_object_name = 'object'  

    def get_queryset(self, request):
        queryset = self.model.objects.all()
        if self.filter_by_user:
            queryset = queryset.filter(user=request.user)
        return self.apply_custom_filters(queryset, request)  

    def apply_custom_filters(self, queryset, request):
        """Hook method for custom filtering in child classes"""
        return queryset

    def get_object(self, request, pk=None):
        if pk:
            return get_object_or_404(self.model, pk=pk)
        return self.get_queryset(request)

    def get(self, request, pk=None):
        result = self.get_object(request, pk)
        # Handle both queryset and dictionary returns
        if isinstance(result, dict):
            context = result
        else:
            context = {self.context_object_name: result}
        return render(request, self.template_name, context)
