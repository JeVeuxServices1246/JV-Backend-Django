from django.conf import settings
from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.db import transaction


def generate_service_data(service_obj):
    service_data = {
        'service_id': service_obj.id,
        'service_name': service_obj.name,
        'service_description': service_obj.description,
        'service_cost': service_obj.cost,
        'service_category_id': service_obj.service_category.id,
        'service_category_name': service_obj.service_category.name,
        'service_image': settings.MEDIA_PATH + service_obj.image
    }
    return service_data


def get_categories(category=None, level=0, include_sub=True, include_services=False):
    if category:
        categories = []
        subcategories = ServiceSubcategory.objects.filter(parent_service_category_id=category.id)
        for cat in subcategories:
            categories.append(cat.service_category)
    else:
        categories = ServiceCategory.objects.exclude(id__in=ServiceSubcategory.objects.values_list('service_category_id', flat=True))

    results = []
    for category in categories:
        services = Service.objects.filter(service_category_id=category.id)
        services_list = []
        for service in services:
            services_list.append(generate_service_data(service))
        result = {
            'id': category.id,
            'name': category.name,
            'description': category.description,
            'image': settings.MEDIA_PATH + category.image,
            'services': services_list
        }
        if include_sub:
            result['subcategories'] = []
        if level > 0:
            subcategories = get_categories(category, level-1)
            result['subcategories'] = subcategories
        results.append(result)

    return results


@api_view(['POST'])
def service_categories(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    level = request.data.get('level', 0)

    try:
        # categories = ServiceCategory.objects.exclude(id__in=ServiceSubcategory.objects.values_list('service_category_id', flat=True))
        include_sub = True if level else False
        categories = get_categories(category=None, level=level, include_sub=include_sub, include_services=True)

        response_data['status'] = True
        response_data['message'] = 'Categories list.'
        response_data['data'] = categories
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def service_subcategories(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    service_category_id = request.data.get('category_id', None)
    level = request.data.get('level', 0)

    if service_category_id:
        try:
            service_category_obj = ServiceCategory.objects.get(id=service_category_id)
            # categories = ServiceSubcategories.objects.filter(parent_service_category_id=service_category_id)
            include_sub = True if level else False
            categories = get_categories(category=service_category_obj, level=level, include_sub=include_sub, include_services=True)

            response_data['status'] = True
            response_data['message'] = 'Categories list.'
            response_data['data'] = categories
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'category_id is mandatory'
    return Response(response_data)


@api_view(['POST'])
def add_service_category(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    name = request.data.get('name', None)
    description = request.data.get('description', None)
    parent_category_ids = request.data.get('parent_category_ids', [])
    image_path = request.data.get('image_path', None)

    try:
        if parent_category_ids:
            with transaction.atomic():
                category_obj = ServiceCategory.objects.create(name=name, description=description, image=image_path)
                for parent_category_id in parent_category_ids:
                    parent_category_obj = ServiceCategory.objects.get(id=parent_category_id)
                    ServiceSubcategory.objects.create(service_category=category_obj,
                                                        parent_service_category=parent_category_obj)
        else:
            category_obj = ServiceCategory.objects.create(name=name, description=description, image=image_path)
        
        response_data['status'] = True
        response_data['message'] = 'Category Added..'
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def update_service_category(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    category_id = request.data.get('category_id', None)
    parent_category_ids = request.data.get('parent_category_ids', [])

    try:
        category_obj = ServiceCategory.objects.get(id=category_id)

        category_obj.name = request.data.get('name', category_obj.name)
        category_obj.description = request.data.get('description', category_obj.description)

        if parent_category_ids:
            with transaction.atomic():
                old_parent_categories = ServiceSubcategory.objects.filter(parent_service_category_id__in=parent_category_ids)
                old_parent_categories.delete()
                for parent_category_id in parent_category_ids:
                    parent_category_obj = ServiceCategory.objects.get(id=parent_category_id)
                    ServiceSubcategory.objects.create(service_category=category_obj,
                                                        parent_service_category=parent_category_obj)

        category_obj.save()

        response_data['status'] = True
        response_data['message'] = 'Category Updated..'
        response_data['data'] = get_categories(category=category_obj.id, level=0)
    except ServiceCategory.DoesNotExist:
        response_data['message'] = f'Category does not exist with id: {category_id}'
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def add_service(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.user_id

    # provider_id = request.data.get('provider_id', None)
    name = request.data.get('name', None)
    description = request.data.get('description', None)
    cost = request.data.get('cost', None)
    image = request.data.get('image_path', None)
    service_category_id = request.data.get('service_category_id', None)

    if user_id and name and cost and service_category_id:
        try:
            user_obj = User.objects.get(id=user_id)
            service_category_obj = ServiceCategory.objects.get(id=service_category_id)

            service_obj = Service.objects.create(created_by=user_obj, service_category=service_category_obj,
                                    name=name, description=description, cost=cost, image=image)

            response_data['status'] = True
            response_data['message'] = "Service added"
            response_data['data'] = generate_service_data(service_obj)
        except User.DoesNotExist:
            response_data['message'] = f'User with given user_id does not exist'
        except ServiceCategory.DoesNotExist:
            response_data['message'] = f'ServiceCategory with given category_id does not exist'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'name, cost and service_category_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def update_service(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    service_id = request.data.get('service_id', None)
    # provider_id = request.data.get('provider_id', None)
    name = request.data.get('name', None)
    description = request.data.get('description', None)
    cost = request.data.get('cost', None)
    image = request.data.get('image_path', None)
    service_category_id = request.data.get('service_category_id', None)

    if service_id:
        try:
            # provider_obj = Providers.objects.get(id=provider_id)
            service_obj = Service.objects.get(id=service_id)

            if name:
                service_obj.name = name
            if description:
                service_obj.description = description
            if cost:
                service_obj.cost = cost
            if image:
                service_obj.image = image
            if service_category_id:
                service_category_obj = ServiceCategory.objects.get(id=service_category_id)
                service_obj.service_category = service_category_obj
            
            service_obj.save()

            response_data['status'] = True
            response_data['message'] = "Service Updated"
            response_data['data'] = generate_service_data(service_obj)
        # except Providers.DoesNotExist:
        #     response_data['message'] = f'Provider with given provider_id does not exist'
        except ServiceCategory.DoesNotExist:
            response_data['message'] = f'ServiceCategory with given category_id does not exist'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'service_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def services(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    category_id = request.data.get('category_id', None)

    try:
        services_list = []
        if category_id:
            services = Service.objects.select_related().filter(service_category_id=category_id)
        else:
            services = Service.objects.select_related().all()
        for service in services:
            services_list.append(generate_service_data(service))

        response_data['status'] = True
        response_data['message'] = 'Services list.'
        response_data['data'] = services_list
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def delete_service(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)
    service_id = request.data.get('service_id', None)

    if user_id and service_id:
        try:
            user_obj = User.objects.get(id=user_id)
            deleted_service_ids = Service.objects.get(created_by=user_obj, id=service_id).delete()

            response_data['status'] = True
            response_data['message'] = "Service is deleted from Cart"
            response_data['data'] = deleted_service_ids
        except User.DoesNotExist:
            response_data['message'] = f'Provide a valid user_id'
        except Service.DoesNotExist:
            response_data['message'] = f'Provide a valid service_id'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and service_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def service_cart(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)

    try:
        services_list = []
        service_cart = ServiceCart.objects.select_related().filter(user_id=user_id)
        for cart_service in service_cart:
            service = cart_service.service
            services_list.append({
                'service_id': service.id,
                'service_name': service.name,
                'service_description': service.description,
                'service_cost': service.cost,
                'service_category_id': service.service_category.id,
                'service_category_name': service.service_category.name
            })

        response_data['status'] = True
        response_data['message'] = 'Services list in user cart'
        response_data['data'] = services_list
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def add_to_cart(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)
    service_id = request.data.get('service_id', None)

    if user_id and service_id:
        try:
            user_obj = User.objects.get(id=user_id)
            service_obj = Service.objects.get(id=service_id)

            ServiceCart.objects.create(user=user_obj, service=service_obj)

            response_data['status'] = True
            response_data['message'] = "Service added to user's cart"
        except User.DoesNotExist:
            pass
        except Service.DoesNotExist:
            pass
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and service_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def save_service_for_later(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)
    service_id = request.data.get('service_id', None)

    if user_id and service_id:
        try:
            service_cart_obj = ServiceCart.objects.get(user=user_id, service=service_id)
            service_cart_obj.show_in_cart = False
            service_cart_obj.save()

            response_data['status'] = True
            response_data['message'] = "Service is hidden from Cart & saved for later"
        except User.DoesNotExist:
            pass
        except Service.DoesNotExist:
            pass
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and service_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def delete_service_from_cart(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)
    service_id = request.data.get('service_id', None)

    if user_id and service_id:
        try:
            service_cart_obj = ServiceCart.objects.get(user=user_id, service=service_id).delete()

            response_data['status'] = True
            response_data['message'] = "Service is deleted from Cart"
        except User.DoesNotExist:
            pass
        except Service.DoesNotExist:
            pass
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and service_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def service_bookings(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)

    try:
        services_list = []
        service_cart = ServiceBooking.objects.select_related().filter(user_id=user_id)
        for cart_service in service_cart:
            service = cart_service.service
            services_list.append({
                'service_id': service.id,
                'service_name': service.name,
                'service_description': service.description,
                'service_cost': service.cost,
                'service_category_id': service.service_category.id,
                'service_category_name': service.service_category.name
            })

        response_data['status'] = True
        response_data['message'] = 'Services booked by user'
        response_data['data'] = services_list
    except BaseException as e:
        response_data['message'] = f'Error: {e}'
    return Response(response_data)


@api_view(['POST'])
def book_service(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)
    service_id = request.data.get('service_id', None)

    if user_id and service_id:
        try:
            user_obj = User.objects.get(id=user_id)
            service_obj = Service.objects.get(id=service_id)

            ServiceBooking.objects.create(user=user_obj, service=service_obj)

            response_data['status'] = True
            response_data['message'] = "Service booked"
        except User.DoesNotExist:
            pass
        except Service.DoesNotExist:
            pass
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and service_id are mandatory'
    return Response(response_data)