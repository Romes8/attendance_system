from herokuapp.models import MyUser, Students, Teachers
from django.core.mail import send_mail


def get_userID_name(role, username):
    try:
        user_id = MyUser.objects.get(username=username).id
        if role == 'student':
            user = Students.objects.get(user_id=user_id)
        else:
            user = Teachers.objects.get(user_id=user_id)
        id = user.id
        name = user.firstname + ' ' + user.lastname
        return id, name
    except:
        raise Exception


def forgot_pass(email):
    user = Students.objects.get(email=email).user
    if user is None:
        user = Teachers.objects.get(email=email).user
    if user:
        print(user)
        send_mail(
            'Reset password for Attendance system KEA',
            'Follow the link to reset your password for user {}'.format(user.username),
            'keaexample5@gmail.com',
            ['{}'.format(email)],
            fail_silently=False,
        )
        return "Succesfully sent"
    return "Error"


def change_pass(username, password):
    username = 'cata0925'
    user = MyUser.objects.get(username=username)
    if user:
        user.set_password(password)
        user.save()
        return "Successfully changed"
    return "Error"
