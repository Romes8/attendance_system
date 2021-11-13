from attendance_app.models import MyUser, Students, Teachers


def get_userID_name(role, username):
    try:
        user_id = MyUser.objects.get(username=username).id
        if role == 'student':
            user = Students.objects.get(user_id=user_id)
        else :
            user = Teachers.objects.get(user_id=user_id)
        id = user.id
        name = user.firstname + ' ' + user.lastname
        return id, name
    except:
        raise Exception
        
