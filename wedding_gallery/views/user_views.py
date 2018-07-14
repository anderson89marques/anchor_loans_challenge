from pyramid.httpexceptions import HTTPFound
from pyramid.security import remember
from pyramid.view import view_config

from wedding_gallery.models import User


class UserView:
    def __init__(self, request):
        self.request = request
        self.session = request.session

    @view_config(route_name='register', renderer='../templates/register.jinja2', request_method='GET')
    def show_register_page(self):
        return {}

    @view_config(route_name='register', request_method='POST')
    def register(self):
        username = self.request.POST['name']
        passwd =  self.request.POST['password']
        pswd_confirm = self.request.POST['confirm']
        err_condition = (passwd != pswd_confirm)
        if err_condition:
            self.session.flash(
                "password and confirm password aren't equal.", queue='error')
            return HTTPFound(location='/register')

        user = User(name=username, role='basic')         
        user.set_password(passwd)
        self.request.dbsession.add(user)

        headers = remember(self.request, user.id)
        return HTTPFound(location='/', headers=headers)
