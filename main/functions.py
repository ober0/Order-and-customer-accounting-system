def addUserData(request, context):
    context['isAdmin'] = request.user.is_staff
    context['username'] = request.user.first_name

    return context