def get_ip(request):
    req_headers = request.META
    str_lista_ip = request.META.get('HTTP_X_FORWARDED_FOR')
    if str_lista_ip:
        return str_lista_ip.split(',')[-1].strip()
    else:
        return request.META.get('REMOTE_ADDR')



class MiddlewareNou:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.ip = get_ip(request)      
        
        response = self.get_response(request)      

        response['header_nou'] = 'valoare'

        return response
