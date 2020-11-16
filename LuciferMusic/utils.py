from LuciferMusic.serializers import UserSerializer
def jwt_response_payload_handler(token, user=None, request=None):
    """
    Returns the response data for both the login and refresh views.
    Override to return a custom response such as including the
    serialized representation of the User.

    Example:

    def jwt_response_payload_handler(token, user=None, request=None):
        return {
            'token': token,
            'user': UserSerializer(user, context={'request': request}).data
        }

    """
    return {
        'token': token,
        'user': UserSerializer(user, context={'request': request}).data
    }

from django.contrib.auth.backends import ModelBackend
from .models import UserProfile as User
from django.db.models import Q


def get_user_by_other_info(account):
    """
    根据不同的账号类型来获取用户
    :param username:  用户信息，可以是用户名，也可以是邮箱或者手机号码
    :return:
    """
    try:
        user = User.objects.get(Q(username=account) | Q(email=account))
    except User.DoesNotExist:
        user = None
    return user


class UserInfoModelBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        重写authentication, 以支持多条件登录
        :param request:
        :param username: 用户名或者手机号码或者用户邮箱
        :param password:  登录密码
        :param kwargs:
        :return: 认证后的用户对象
        """
        user = get_user_by_other_info(username)
        # print(isinstance(user, User))
        # print(password)
        # print(user.check_password(password))
        # print(self.user_can_authenticate(user))
        if isinstance(user, User) and user.check_password(password) and self.user_can_authenticate(user):
            return user