#todolist context procesor

def user_id(request):
    if request.user.is_authenticated:
        return {'user_id' : request.user.id,
                'task_count': request.user.todolists.count(),
                'task_important_count': request.user.todolists.filter(important=True).count()}
    return {'user_id' : None}