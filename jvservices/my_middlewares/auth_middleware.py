import time
from django.http import HttpResponse
import jwt
from django.conf import settings

def jwt_auth(get_response):
    # One-time configuration and initialization.

    def middleware(request):
        start_time = time.time()
        api_name = request.path.split('/')[-2]
        # print(api_name, ' : api_name ', request.path.split('/'), request.path)
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        direct_urls = ['send_otp', 'login', 'register', 'reset_password', 'send_smtp_email']

        if api_name in direct_urls:
            response = get_response(request)
        else:
            response = HttpResponse('you are not authorized to send this request.')
            try:
                jwt_token = request.headers.get('Authorization', None)
                if jwt_token:
                    try:
                        decoded = jwt.decode(jwt_token.split(' ')[1], settings.SECRET_KEY, algorithms=['HS256'])
                        decoded_user_id = decoded.get('user_id', None)
                        request.user_id = decoded_user_id
                        response = get_response(request)
                    except jwt.ExpiredSignatureError:
                        response = HttpResponse('Token has expired')
                    except jwt.InvalidSignatureError:
                        response = HttpResponse('Token signature is invalid')
                    except BaseException as je:
                        print(f'Error decoding token : {je}')
            except BaseException as e:
                print('Error : {e}')

        # Code to be executed for each request/response after
        # the view is called.

        print(f"{api_name}/ completed in %s seconds {time.time() - start_time}")

        return response

    return middleware



# from django.core.cache import cache
# import time
# import json

# def view_cache(get_response):
#     # One-time configuration and initialization.
#     def middleware(request):
#         start_time = time.time()
#         api_name = request.path.split('/')[-2]
#         payload_str = request.body.decode("utf-8")
#         cache_key = api_name + payload_str
#         cache_data = cache.get(cache_key)

#         saving_views = ['user_login', 'update_gst_company_user']

#         ignore_cache = [] # ['get_all_other_itc_data', 'get_2b_reconciliation_report']

#         not_allow_cache = api_name in saving_views

#         # Code to be executed for each request before
#         # the view (and later middleware) are called.
#         if cache_data and (not not_allow_cache):
#             response = cache_data
#             print(f'hurray..! cache found for {cache_key} ..')
#         else:
#             response = get_response(request)
#             if not_allow_cache:
#                 cache.clear()
#                 print('cache cleared.. hmm..! ')
#             elif api_name in ignore_cache:
#                 print(f'cache ignored for {cache_key}')
#             else:
#                 try:
#                     cache.set(cache_key, response)
#                     print(f'fine.. cache saved for {cache_key}')
#                 except BaseException as e:
#                     print(f'exception for {cache_key} error : {e}')
#         # Code to be executed for each request/response after
#         # the view is called.
#         # response = get_response(request)
#         print("completed in %s seconds" % (time.time() - start_time))
#         return response
#     return middleware