import os

from fs_s3fs import S3FS
from fs.errors import ResourceError
from minio import Minio
from celery import shared_task


def fs_server(bucket_name):
    return S3FS(
            bucket_name=f'user{bucket_name}', aws_access_key_id=os.environ.get("MINIO_ROOT_USER"),
            aws_secret_access_key=os.environ.get("MINIO_ROOT_PASSWORD"), endpoint_url='http://minio:9000/'
        )


@shared_task
def upload_to_minio(bucket_name, file_name, file_path):
    client = Minio("minio:9000/",
                   access_key=os.environ.get("MINIO_ROOT_USER"),
                   secret_key=os.environ.get("MINIO_ROOT_PASSWORD"),
                   secure=False)
    if not client.bucket_exists(bucket_name):
        client.make_bucket(bucket_name)
    client.fput_object(bucket_name=bucket_name, object_name=file_name, file_path=file_path)
    if file_path not in ('file_storage/test_download', 'file_storage/test_upload'):
        os.remove(file_path)

@shared_task
def list_files(bucket_name):
    try:
        fs = fs_server(bucket_name)
        return fs.listdir('/')
    except ResourceError:
        return None


@shared_task
def download_files(bucket_name, files):
    fs = fs_server(bucket_name)
    dict_of_urls = {}
    # получение хост адреса для формирования ссылок на скачивание
    get_host = str(os.environ.get("DJANGO_ALLOWED_HOSTS")).split(" ")[0]
    for file in files:
        url = str(fs.geturl(file, 'download')).replace('minio', get_host, 1)
        dict_of_urls.update({file: url})
    return dict_of_urls
