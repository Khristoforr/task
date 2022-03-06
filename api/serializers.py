from rest_framework import serializers
from .models import File


class FileSerializer(serializers.ModelSerializer):

    class Meta:
        model = File
        fields = '__all__'
        read_only_fields = ['file_size', 'file_type', 'owner', 'file_name']

    def to_representation(self, instance):
        rep = {"Status": True,
               "Загружен файл": instance.file_name,
               "Размер": f'{instance.file_size}МБ'}
        return rep
