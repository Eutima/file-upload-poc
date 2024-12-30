from rest_framework import serializers
from . models import File
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser, FileUploadParser
from rest_framework import status
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import ValidationError
import logging
import traceback
import base64
from django.core.files.base import ContentFile

logger = logging.getLogger(__name__)


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']


class Base64FileSerializer(serializers.ModelSerializer):
    file = serializers.CharField(write_only=True)

    class Meta:
        model = File
        fields = ['id', 'file', 'uploaded_at']

    def create(self, validated_data):
        file_data = validated_data.pop('file')
        format, file_str = file_data.split(
            ';base64,') if ';base64,' in file_data else (None, file_data)
        file_name = "uploaded_file.bin"  # Provide a default file name
        decoded_file = ContentFile(base64.b64decode(file_str), name=file_name)

        return File.objects.create(file=decoded_file)


class FileUploadView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    # parser_classes = [FileUploadParser]

    def post(self, request, *args, **kwargs):

        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileUploadB64ViewSet(ModelViewSet):
    queryset = File.objects.all()
    serializer_class = Base64FileSerializer
    # parser_classes = [MultiPartParser, FormParser]


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
                data={'validation error': f'{e}'},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            logger.error(f'upload failed {e}')
            return Response(
                data={'unexpected error': f'{e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        except:
            traceback.print_exc()
            return Response(
                data={'unexpected error': f'{e}'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        finally:
            logger.info('request handling completed')
