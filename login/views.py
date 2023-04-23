from django.conf import settings
from django.db import connection
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import *
from django.db import IntegrityError

import time
from datetime import datetime, timedelta
import jwt
import requests
import random
import json
import bcrypt
salt = bcrypt.gensalt()

import sib_api_v3_sdk
from sib_api_v3_sdk.rest import ApiException

from jvservices.utils.helpers import send_email


def generate_token(user_data, login_type='app'):
    jwt_payload = user_data.copy()
    if login_type.lower() != 'app':
        tomorrow_date = datetime.now() + timedelta(hours=24)
        jwt_payload['exp'] = tomorrow_date
    token = jwt.encode(jwt_payload, settings.SECRET_KEY, algorithm="HS256")
    return token

def generate_user_data(user_obj):
    user_data = {
        'user_id': user_obj.id, 'country_code': user_obj.country_code, 'phone_number': user_obj.phone_number, 
        'username': user_obj.username, 'first_name': user_obj.first_name, 'last_name': user_obj.last_name,
        'email': user_obj.email, 'profile_pic': user_obj.profile_pic, 'email_verified': user_obj.email_verified
    }
    return user_data

def generate_provider_data(provider_obj):
    user_data = generate_user_data(provider_obj.user)
    provider_data = {
        'provider_id': provider_obj.id,
        'dl_front_image': settings.MEDIA_PATH + provider_obj.dl_front_image, 
        'dl_back_image': settings.MEDIA_PATH + provider_obj.dl_back_image,
        'status': provider_obj.status, 'is_active': provider_obj.is_active 
    }
    provider_data.update(user_data)
    return provider_data

def generate_address_data(address_obj):
    address_data = {
        "address_id": address_obj.id, "street_address": address_obj.street_address,
        "house_number": address_obj.house_number, "city": address_obj.city,
        "state": address_obj.state, "zip_code": address_obj.zip_code
    }
    return address_data


@api_view(['GET'])
def index(request):
    res = {'status': True, "message": "This Project is developed & deployed by SivaPrasad (SP)"}
    with connection.cursor() as cursor:
        cursor.execute("select * from users limit 1")
        users = cursor.fetchall()
    res['data'] = users
    return Response(res)


@api_view(['POST'])
def send_otp(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    phone_number = request.data.get('phone_number', None)
    cc = request.data.get('country_code', '1')
    forgot_password = request.data.get('forgot_password', False)

    if phone_number:
        try:
            if not forgot_password:
                try:
                    User.objects.get(phone_number=phone_number)
                    response_data['message'] = 'phone_number already exists'
                    return Response(response_data)
                except:
                    pass
            
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'
            api_instance = sib_api_v3_sdk.TransactionalSMSApi(sib_api_v3_sdk.ApiClient(configuration))

            otp = random.randint(1000,9999)
            if cc == 91 or cc == '91':
                sms_text = f'OTP from JV Services to verify your phone_number number is {otp}'
            else:
                sms_text = f'Utilisez le code à usage unique code {otp} pour vérifier votre téléphone'

            send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender="JVS", recipient=f'{cc}{phone_number}', content=sms_text, type="transactional")
            api_response = api_instance.send_transac_sms(send_transac_sms)

            if api_response:
                response_data['status'] = True
                response_data['message'] = 'OTP sent'
                response_data['data'] = {'otp': otp}
            else:
                print(f'Response Error: {api_response}')
                response_data['message'] = 'Error sending OTP, try again later.'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'phone_number is mandatory'
    return Response(response_data)


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

@api_view(['POST'])
def send_smtp_email(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    # Email configuration
    sender = 'team@jvservices.ca'
    recipient = request.data.get('email', 'sivaprasad.student@gmail.com')
    subject = 'Test Email'
    message = 'This is a test email sent using SMTP authentication in Python'

    # SMTP server configuration
    smtp_server = 'rs9-nyc.serverhostgroup.com'
    smtp_port = 465
    smtp_username = 'team@jvservices.ca'
    smtp_password = 'Django@project1'

    # Create a MIME message
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    try:
        # Connect to the SMTP server and send the email
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(smtp_username, smtp_password)
            smtp.sendmail(sender, recipient, msg.as_string())
            response_data['status'] = True
            response_data['message'] = 'Email sent'
    except BaseException as e:
        response_data['message'] = f"Error: {e}"
    return Response(response_data)


@api_view(['POST'])
def send_otp_to_email(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    email = request.data.get('email', None)
    forgot_password = request.data.get('forgot_password', False)

    if email:
        try:
            if not forgot_password:
                try:
                    User.objects.get(email=email)
                    response_data['message'] = 'email already exists'
                    return Response(response_data)
                except:
                    pass
            
            otp = random.randint(1000,9999)
            # sms_text = f'OTP from JV Services to verify your email is {otp}'
            # sms_url = f'https://api.smsala.com/api/SendSMS?api_id=API1230366295727&api_password=qwerty123&sms_type=P&encoding=T&sender_id=info&phonenumber=1{phone_number}&textmessage={sms_text}'
            # sms_response = requests.get(sms_url)
            configuration = sib_api_v3_sdk.Configuration()
            configuration.api_key['api-key'] = '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'

            api_instance = sib_api_v3_sdk.TransactionalEmailsApi(sib_api_v3_sdk.ApiClient(configuration))
            subject = 'OTP to verify' #subject
            html_content = f'<b>Your OTP is {otp}</b>' #message
            # textContent = 'only text..'
            sender = {"name": 'Jvs', "email": 'team@jvservices.ca'}
            to = [{"email": email}] #'sivaprasad.student@gmail.com' # {"email": email, "name": '_SP'}
            headers = {"Some-Custom-Name": "unique-id-1234"}

            # attachments = [
            #     {"url": "https://www.africau.edu/images/default/sample.pdf", "name": "attachment1.pdf"},
            #     # {"url": "https://marketplace.canva.com/EAFC1OcYOM0/2/0/1131w/canva-black-white-minimalist-simple-creative-freelancer-invoice-pyLVaYlAk1o.jpg", "name": "test_img.jpg"}
            # ]

            # send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, template_id=2, params={
            #     'name': 'SP',
            #     'test_id': '12345'
            # }, attachment=attachments, sender=sender, subject=subject)

            # send_transac_sms = sib_api_v3_sdk.SendTransacSms(sender="SP", recipient="919550531453", content="OTP is 9900", type="transactional")
            send_smtp_email = sib_api_v3_sdk.SendSmtpEmail(to=to, headers=headers, html_content=html_content, sender=sender, subject=subject)

            api_response = api_instance.send_transac_email(send_smtp_email)

            if api_response:
                response_data['status'] = True
                response_data['message'] = 'OTP sent'
                response_data['data'] = {'otp': otp}
            else:
                print(f'Response Error: {api_response}')
                response_data['message'] = 'Error sending OTP, try again later.'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'email is mandatory'
    return Response(response_data)


@api_view(['POST'])
def register(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    country_code = request.data.get('country_code', 1)
    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)
    username = request.data.get('username', None)
    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    email = request.data.get('email', None)
    profile_pic = request.data.get('profile_pic', None)
    fcm_token = request.data.get('fcm_token', None)

    print(f'fcm_token : {fcm_token}')

    if phone_number and password and first_name:
        try:
            password_bytes = b'' + password.encode('utf-8')
            hashed_password = str(bcrypt.hashpw(password_bytes, salt))[2:-1]

            if username:
                username = username.lower()

            user_obj = User.objects.create(country_code=country_code, phone_number=phone_number, password=hashed_password,
                                            fcm_token=fcm_token, first_name=first_name, last_name=last_name, email=email,
                                            profile_pic=profile_pic, username=username)
            
            if username is None:
                seq = user_obj.id + 99
                while User.objects.filter(username=username).exists():
                    seq += 1
                username = f'{first_name.replace(" ", "").lower()}{seq}'
                user_obj.save()

            user_data = generate_user_data(user_obj)

            token = generate_token(user_data)

            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = {
                'user_data': user_data,
                'token': token
            }
        except IntegrityError as ie:
            dup_err = str(ie)
            print(dup_err)
            if 'phone_number' in dup_err:
                response_data['message'] = f'phone_number already exists'
            elif 'email' in dup_err:
                response_data['message'] = f'email already exists'
            elif 'username' in dup_err:
                response_data['message'] = f'username already exists'
            else:
                response_data['message'] = f'Duplicate: {ie}'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'first_name, phone_number and password are mandatory'
    return Response(response_data)


@api_view(['POST'])
def reset_password(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)

    if phone_number and password:
        try:
            password_bytes = b'' + password.encode('utf-8')
            hashed_password = str(bcrypt.hashpw(password_bytes, salt))[2:-1]

            user_obj = User.objects.get(phone_number=phone_number)

            user_obj.password = hashed_password
            user_obj.save()

            user_data = generate_user_data(user_obj)

            token = generate_token(user_data)

            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = {
                'user_data': user_data,
                'token': token
            }
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'name, phone_number and password are mandatory'
    return Response(response_data)


@api_view(['POST'])
def login(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    phone_number = request.data.get('phone_number', None)
    password = request.data.get('password', None)
    fcm_token = request.data.get('fcm_token', None)
    login_type = request.data.get('login_type', 'app')

    print(f'fcm_token : {fcm_token}')

    if phone_number and password:
        try:
            user_obj = User.objects.get(phone_number=phone_number)

            hashed_password = user_obj.password
            password_bytes = b'' + password.encode('utf-8')
            # print(bcrypt.checkpw(b'sp123', b'' + '$2y$10$.DfZTjn/r0yOfeC7HTlLXuViqbSOsL0tSEor611M2R9cPCtnL6h3m'.encode('utf-8')), '........')

            if bcrypt.checkpw(password_bytes, b''+ hashed_password.encode('utf-8')):
                user_data = generate_user_data(user_obj)
                token = generate_token(user_data, login_type)

                if fcm_token:
                    user_obj.fcm_token = fcm_token
                    user_obj.last_login = datetime.now()
                    user_obj.save()

                response_data['status'] = True
                response_data['message'] = 'Success'
                response_data['data'] = {
                    'user_data': user_data,
                    'token': token
                }
            else:
                response_data['message'] = 'Password mismatch'
        except User.DoesNotExist:
            response_data['message'] = f'No account with {phone_number}'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'phone_number and password are mandatory'
    return Response(response_data)


@api_view(['POST'])
def update_profile(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    user_id = request.data.get('user_id', request.user_id)

    first_name = request.data.get('first_name', None)
    last_name = request.data.get('last_name', None)
    email = request.data.get('email', None)
    username = request.data.get('username', None)
    profile_pic = request.data.get('profile_pic', None)
    fcm_token = request.data.get('fcm_token', None)

    if user_id:
        try:
            user_obj = User.objects.get(id=user_id)

            user_obj.first_name = first_name if first_name else user_obj.first_name
            user_obj.last_name = last_name if last_name else user_obj.last_name
            user_obj.email = email if email else user_obj.email
            user_obj.username = username if username else user_obj.username
            user_obj.profile_pic = profile_pic if profile_pic else user_obj.profile_pic
            user_obj.fcm_token = fcm_token if fcm_token else user_obj.fcm_token
            user_obj.save()

            user_data = generate_user_data(user_obj)

            token = generate_token(user_data)

            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = {
                'user_data': user_data,
                'token': token
            }
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'You are not allowed to update'
    return Response(response_data)


@api_view(['POST'])
def validate_username(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    username = request.data.get('username', None)

    if username:
        username = username.replace(" ", "").lower()
        try:
            User.objects.get(username=username)
            response_data['status'] = True
            response_data['message'] = 'Username already Exists'
            response_data['data'] = {'is_valid': False, 'username': username}
        except User.DoesNotExist:
            response_data['status'] = True
            response_data['message'] = 'Username does not Exist'
            response_data['data'] = {'is_valid': True, 'username': username}
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'username is mandatory'
    return Response(response_data)

@api_view(['GET'])
def users(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    try:
        users = User.objects.all()

        users_data = []

        for user in users:
            users_data.append(generate_user_data(user))

        response_data['status'] = True
        response_data['message'] = 'users data fetched'
        response_data['data'] = users_data
    except BaseException as e:
        response_data['message'] = f'Error {e}'

    return Response(response_data)


@api_view(['GET'])
def providers(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    try:
        providers = Provider.objects.all()

        providers_data = []

        for provider in providers:
            providers_data.append(generate_provider_data(provider))

        response_data['status'] = True
        response_data['message'] = 'Providers data fetched'
        response_data['data'] = providers_data
    except BaseException as e:
        response_data['message'] = f'Error {e}'

    return Response(response_data)


@api_view(['POST'])
def register_provider(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    user_id = request.data.get('user_id', None)
    service_category_ids = request.data.get('service_category_ids', [])
    dl_front_image = request.data.get('dl_front_image', None)
    dl_back_image = request.data.get('dl_back_image', None)
    latitude = request.data.get('latitude', None)
    longitude = request.data.get('longitude', None)
    service_range = request.data.get('service_range', 0)

    if user_id and dl_front_image and dl_back_image:
        try:
            user_obj = User.objects.get(id=user_id)
            provider_obj = Provider.objects.create(user=user_obj,
                            dl_front_image=dl_front_image, dl_back_image=dl_back_image,
                            latitude=latitude, longitude=longitude, service_range=service_range)

            for service_category_id in service_category_ids:
                service_category_obj = ServiceCategory.objects.get(id=service_category_id)
                ProviderServiceCategory.objects.create(provider=provider_obj, service_category=service_category_obj)

            response_data['status'] = True
            response_data['message'] = 'Provider added'

            user_email = user_obj.email
            if user_email:
                email_response = send_email({ 'name': user_obj.first_name, 'email': user_obj.email })
                if email_response['status']:
                    response_data['message'] += ' & email sent'
            
            response_data['data'] = generate_provider_data(provider_obj)
        except User.DoesNotExist:
            response_data['message'] = f'{user_id} is not a valid user_id'
        except IntegrityError as ie:
            print(f'Integrity Error: {ie}')
            response_data['message'] = f'provider already exists'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id, dl_front_image and dl_back_image are mandatory'

    return Response(response_data)


@api_view(['POST'])
def provider_info(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    user_id = request.data.get('user_id', None)

    if user_id:
        try:
            provider_obj = Provider.objects.get(user_id=user_id)

            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['data'] = generate_provider_data(provider_obj)
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id is mandatory'

    return Response(response_data)


@api_view(['POST'])
def update_provider(request):
    response_data = {'status': False, 'message': 'Something went wrong'}

    user_id = request.data.get('user_id', None)

    if user_id:
        try:
            provider_obj = Provider.objects.get(user_id=user_id)

            provider_obj.dl_front_image = request.data.get('dl_front_image', provider_obj.dl_front_image)
            provider_obj.dl_back_image = request.data.get('dl_back_image', provider_obj.dl_back_image)
            provider_obj.status = request.data.get('status', provider_obj.status)
            provider_obj.is_active = request.data.get('is_active', provider_obj.is_active)

            provider_obj.save()

            response_data['status'] = True
            response_data['message'] = 'Provider info Updated..'
            response_data['data'] = generate_provider_data(provider_obj)
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id is mandatory.'
    return Response(response_data)


@api_view(['POST'])
def delete_user(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    user_id = request.data.get('user_id', None)
    phone_number = request.data.get('phone_number', None)

    if user_id or phone_number:
        try:
            if user_id:
                deleted_user_id = User.objects.filter(id=user_id).delete()[0]
            else:
                deleted_user_id = User.objects.filter(phone_number=phone_number).delete()[0]
            
            response_data['status'] = True
            if deleted_user_id:
                response_data['message'] = 'Success, deleted'
            else:
                response_data['message'] = 'Phone_number does not exist'
        except User.DoesNotExist:
            response_data['message'] = f'User with phone_number {phone_number} not found.'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id or phone_number are mandatory'
    return Response(response_data)


@api_view(['POST'])
def delete_provider(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    user_id = request.data.get('user_id', None)

    if user_id:
        try:
            provider_obj = Provider.objects.get(user_id=user_id)
            provider_obj.is_active = False
            provider_obj.save()
            
            response_data['status'] = True
            response_data['message'] = 'Success, Provider is removed'
        except User.DoesNotExist:
            response_data['message'] = f'User with user_id {user_id} not found.'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id is mandatory'
    return Response(response_data)


@api_view(['POST'])
def update_user_role(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}

    role_id = request.data.get('role_id', None)
    user_id = request.data.get('user_id', None)

    if role_id and user_id:
        try:
            user_obj = User.objects.get(id=user_id)
            user_obj.role_id = role_id
            user_obj.save()
            
            response_data['status'] = True
            response_data['message'] = 'Success'
        except User.DoesNotExist:
            response_data['message'] = f'User with {user_id} not found.'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'role_id and user_id are mandatory'
    return Response(response_data)


@api_view(['POST'])
def add_user_address(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    user_id = request.data.get('user_id', None)
    street_address = request.data.get('street_address', None)
    house_number = request.data.get('house_number', None)
    city = request.data.get('city', None)
    state = request.data.get('state', None)
    zip_code = request.data.get('zip_code', None)

    if user_id and street_address and house_number and city and state and zip_code:
        try:
            user_obj = User.objects.get(id=user_id)

            address = UserAddress.objects.create(user=user_obj, street_address=street_address, city=city,
                                       house_number=house_number, state=state, zip_code=zip_code)

            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['message'] = generate_address_data(address)
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id, street_address, house_number, city, state and zip_code are mandatory'

    return Response(response_data)


@api_view(['POST'])
def update_user_address(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    user_id = request.data.get('user_id', None)
    address_id = request.data.get('address_id', None)

    street_address = request.data.get('street_address', None)
    house_number = request.data.get('house_number', None)
    city = request.data.get('city', None)
    state = request.data.get('state', None)
    zip_code = request.data.get('zip_code', None)    

    if user_id and address_id:
        try:
            address = UserAddress.objects.get(id=address_id)
            
            if address.user_id == user_id:
                address.street_address = street_address if street_address else address.street_address
                address.house_number = house_number if house_number else address.house_number
                address.city = city if city else address.city
                address.state = state if state else address.state
                address.zip_code = zip_code if zip_code else address.zip_code
                
                address.save()

                response_data['status'] = True
                response_data['message'] = 'Success'
                response_data['data'] = generate_address_data(address)
            else:
                response_data['message'] = f'You are not correct user to edit this Address'
        except UserAddress.DoesNotExist:
            response_data['message'] = f'No address with id {address_id}'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and address_id are mandatory'

    return Response(response_data)


@api_view(['POST'])
def delete_user_address(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    user_id = request.data.get('user_id', None)
    address_id = request.data.get('address_id', None)

    if user_id and address_id:
        try:
            address = UserAddress.objects.get(id=address_id)
            
            if address.user_id == user_id:
                address.delete()

                response_data['status'] = True
                response_data['message'] = 'Success'
            else:
                response_data['message'] = f'You are not correct user to edit this Address'
        except UserAddress.DoesNotExist:
            response_data['message'] = f'No address with id {address_id}'
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id and address_id are mandatory'

    return Response(response_data)


@api_view(['POST'])
def user_addresses(request):
    response_data = { 'status': False, 'message': 'Something went wrong..'}
    
    user_id = request.data.get('user_id', None)

    if user_id:
        try:
            user_addresses = UserAddress.objects.filter(user_id=user_id)

            user_address_list = []

            for address in user_addresses:
                user_address_list.append(generate_address_data(address))

            response_data['status'] = True
            response_data['message'] = 'Success'
            response_data['message'] = user_address_list
        except BaseException as e:
            response_data['message'] = f'Error: {e}'
    else:
        response_data['message'] = 'user_id is mandatory'

    return Response(response_data)