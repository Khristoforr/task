from django.db import IntegrityError
from django.http import JsonResponse
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from .models import File
from .serializers import FileSerializer
from .tasks import list_files, upload_to_minio, download_files


class UploadFileViewSet(ModelViewSet):
    """
    Класс для загрузки файлов на сервер
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['post', ]

    def perform_create(self, serializer):
        try:
            file = self.request.FILES.popitem()[1][0]
            serializer.save(file_name=file.name,
                            owner_id=self.request.user.id,
                            file_size=round(file.size/1000000, 2),
                            file_type=file.content_type)
            upload_to_minio.delay(f'user{self.request.user.id}', file.name, file.temporary_file_path())

        except KeyError:
            raise ValidationError({"Status": False, "Errors": "Пожалуйста, отправьте файл"})

        except IntegrityError:
            raise ValidationError({"Status": False, "Errors": "Файл с таким именем уже загружен"})


class ListFiles(APIView):
    """
    Класс для вывода списка файлов, загруженных пользователем
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        files_list = list_files.delay(self.request.user.id).get()
        if files_list is None:
            return JsonResponse({"Status": False, "Errors": "У вас нет загруженных файлов"})
        files_dict = dict(zip([i for i in range(1, len(files_list) + 1)], files_list))
        return JsonResponse({"Status": True} | files_dict)


class DownloadFiles(APIView):
    """
    Класс для загрузки файлов
    """
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        files_list = list_files.delay(self.request.user.id).get()
        if files_list is None:
            return JsonResponse({"Status": False, "Errors": "У вас нет загруженных файлов"})
        dict_of_urls = download_files.delay(self.request.user.id, files_list).get()
        return JsonResponse({"Status": True} | dict_of_urls)
