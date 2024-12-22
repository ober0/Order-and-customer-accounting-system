def addUserData(request, context):
    context['isAdmin'] = request.user.is_staff
    context['username'] = request.user.first_name
    context['name'] = request.user.first_name + ' ' + request.user.last_name
    return context