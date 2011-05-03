'''
Created on 03.05.2011

@author: D_Unusov
'''
def user(request):
    if hasattr(request, 'user'):
        return {'user':request.user }
    return {}
