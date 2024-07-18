#todolist context procesor

def user_id(request):
    if request.user.is_authenticated:
        return {'user_id' : request.user.id}
    return {'user_id' : None}