from rest_framework.response import Response
from rest_framework.decorators import api_view

import time
from django.core.files.storage import FileSystemStorage

from django.conf import settings
from services.models import Service

from services.views import generate_service_data, get_categories
from .models import *


def generate_banner_data(banner_obj):
    banner_data = {
        'id': banner_obj.id,
        'name': banner_obj.name,
        'description': banner_obj.description,
        'image': settings.MEDIA_PATH + banner_obj.image,
        'url': banner_obj.url,
        # 'expiry_time': banner_obj.expiry_time
    }
    return banner_data

@api_view(['GET'])
def home(request):
    response_data = {'status': False, 'message': 'Something went wrong'}
    try:
        data = {}
        data['categories'] = get_categories(category=None, level=1)
        services_list = []
        services = Service.objects.select_related().all()
        for service in services:
            services_list.append(generate_service_data(service))
        data['services'] = services_list
        banners = Banner.objects.all()
        banners_list = []
        if banners:
            for banner in banners:
                banners_list.append(generate_banner_data(banner))
        data['banners'] = banners_list

        response_data['status'] = True
        response_data['message'] = 'Home page data'
        response_data['data'] = data
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['GET'])
def banners(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    try:
        banners = Banner.objects.all()
        banners_list = []
        if banners:
            for banner in banners:
                banners_list.append(generate_banner_data(banner))
        
        response_data['status'] = True
        response_data['message'] = 'Success'
        response_data['data'] = banners_list
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def add_banner(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    name = request.data.get('name', None)
    description = request.data.get('description', None)
    image = request.data.get('image', None)
    url = request.data.get('url', None)

    if name and description and image:
        try:
            banner_obj = Banner.objects.create(name=name, description=description, image=image, url=url)
            banner_data = generate_banner_data(banner_obj)
            
            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = banner_data
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'name, description and image are mandatory.'
    return Response(response_data)


@api_view(['POST'])
def update_banner(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    banner_id = request.data.get('banner_id', None)
    name = request.data.get('name', None)
    description = request.data.get('description', None)
    image = request.data.get('image', None)
    url = request.data.get('url', None)

    if banner_id and name and description and image:
        try:
            banner_obj = Banner.objects.get(id=banner_id)

            banner_obj.name = name if name else banner_obj.name
            banner_obj.description = description if description else banner_obj.description
            banner_obj.image = image if image else banner_obj.image
            banner_obj.url = url if url else banner_obj.url

            banner_obj.save()

            banner_data = generate_banner_data(banner_obj)
            
            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = banner_data
        except Banner.DoesNotExist:
            response_data['message'] = f'Banner does not exist with id: {banner_id}'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'banner_id, name, description and image are mandatory.'
    return Response(response_data)


@api_view(['POST'])
def delete_banner(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    banner_id = request.data.get('banner_id', None)

    if banner_id:
        try:
            Banner.objects.get(id=banner_id).delete()
            
            response_data['status'] = True
            response_data['message'] = 'Success'
        except Banner.DoesNotExist:
            response_data['message'] = f'Banner does not exist with id: {banner_id}'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'banner_id is mandatory.'
    return Response(response_data)


@api_view(['POST'])
def upload_image(request):
    response_data = {'status': False, 'message': 'Something went wrong'}
    image_category = request.data.get('image_category', 'others')
    folder = image_category + '/'
    if request.FILES['image']:
        try:
            image = request.FILES['image']
            fs = FileSystemStorage(location=settings.MEDIA_ROOT + folder)

            exts = ['jpg', 'jpeg', 'png', 'gif']

            img_name = image.name
            img_strings = img_name.split('.')
            img_ext = img_strings[-1]

            if img_ext in exts:
                img_name = img_name[:-(len(img_ext)+1)]
            
            img_name += '_' + str(int(time.time())) + '.' + img_ext

            saved_img_name = fs.save(img_name, image)
            response_data['status'] = True
            response_data['message'] = "Upload successful"
            response_data['image_url'] = folder + saved_img_name
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = "Provide a valid file with image as key name"
    return Response(response_data)


@api_view(['POST'])
def add_project_module(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    name = request.data.get('name', None)
    description = request.data.get('description', None)

    if name:
        try:
            module_obj = ProjectModule.objects.create(name=name, description=description)
            
            response_data['status'] = True
            response_data['message'] = 'Module Added..'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'name is mandatory'
    return Response(response_data)


@api_view(['POST'])
def add_user_permission(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_role_id = request.data.get('user_role_id', None)
    project_module_id = request.data.get('project_module_id', None)
    can_view = request.data.get('can_view', True)
    can_edit = request.data.get('can_edit', False)
    can_create = request.data.get('can_create', False)
    can_delete = request.data.get('can_delete', False)

    if user_role_id and project_module_id:
        try:
            permission_obj = UserPermission.objects.create(user_role_id=user_role_id, project_module_id=project_module_id,
                    can_view=can_view, can_edit=can_edit, can_create=can_create, can_delete=can_delete)
            
            response_data['status'] = True
            response_data['message'] = 'Permissions added.'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'name is mandatory'
    return Response(response_data)


@api_view(['GET'])
def user_permissions(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    try:
        permissions = UserPermission.objects.all()

        permissions_data = []
        for permission in permissions:
            permissions_data.append({
                "user_role_id": permission.user_role_id,
                "user_role_name": permission.user_role.name,
                "project_module_id": permission.project_module_id,
                "project_module_name": permission.project_module.name,
                "can_view": permission.can_view,
                "can_edit": permission.can_edit,
                "can_create": permission.can_create,
                "can_delete": permission.can_delete
            })
        response_data['status'] = True
        response_data['message'] = 'Success'
        response_data['data'] = permissions_data
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)