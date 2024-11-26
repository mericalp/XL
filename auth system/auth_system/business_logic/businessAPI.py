from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt


@method_decorator(csrf_exempt, name='dispatch')
class EntityAPI(APIView):
    model = None
    serializer_class = None
    filter_by_user = False
    filter_fields = []

    def get_existing_record(self, request, data):
        """Override this method for custom record lookup"""
        return None

    def get_queryset(self, request):
        queryset = self.model.objects.all()
        if self.filter_by_user:
            queryset = queryset.filter(user=request.user)
        for field in self.filter_fields:
            value = request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{field: value})
        return queryset

    def get_object(self, request, pk=None):
        if pk:
            return get_object_or_404(self.model, pk=pk)
        return self.get_queryset(request).first()

    def get(self, request, *args, **kwargs):
        data = request.query_params
        existing_record = self.get_existing_record(request, data)
        if existing_record is not None:
            serializer = self.serializer_class(existing_record, many=True)
        else:
            queryset = self.get_queryset(request)
            serializer = self.serializer_class(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, pk=None):
        data = request.data
        data['user'] = request.user.id  # Dynamically add the user
        print("Payload data:", data)  # Debugging

        existing_record = self.get_existing_record(request, data)
        if existing_record:
            serializer = self.serializer_class(existing_record, data=data, partial=True)
        else:
            serializer = self.serializer_class(data=data, context={'action': data.get('action')})

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
 