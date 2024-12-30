from rest_framework import serializers
from . models import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request, *args, **kwargs):

        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = FileSerializer
    parser_classes = [MultiPartParser, FormParser]

    def create(self, request, *args, **kwargs):
        logger.info('upload started')
        try:
            response = super().create(request, *args, *kwargs)
            logger.info('upload completed')
            return response
        except ValidationError as e:
            return Response(
                data={'unexpected error': f'{e}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f'upload failed {e}')
            return Response(
                data={'unexpected error': f'{e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            logger.info('request handling completed')
