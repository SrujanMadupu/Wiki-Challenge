from rest_framework.response import Response
from rest_framework import status


def check_post_keys(*req_args, **req_keys):
    def outer_wrapper(f):
        def inner_wrapper(cls, request, *args, **kwargs):
            print(">>> big wrapper keys >> ", req_keys)
            print(">>> request data keys >>>> ", request.data.keys())
            for key in req_keys['required_keys']:
                if key not in request.data.keys() or request.data[key] == "":
                    return Response({'KeyError': key+" is required"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return f(cls, request, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper


def check_get_params(*req_args, **req_keys):
    def outer_wrapper(f):
        def inner_wrapper(cls, request, *args, **kwargs):
            print(">>> big wrapper keys >> ", req_keys)
            print(">>> request params >>>> ", request.query_params)
            for key in req_keys['required_keys']:
                if key not in request.query_params.keys() or request.query_params[key] == "":
                    return Response({'KeyError': key+" is required"}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return f(cls, request, *args, **kwargs)
        return inner_wrapper
    return outer_wrapper
