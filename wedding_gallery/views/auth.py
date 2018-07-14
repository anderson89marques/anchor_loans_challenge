import logging

from pyramid.httpexceptions import HTTPFound
from pyramid.security import forget, remember
from pyramid.view import forbidden_view_config, view_config

from wedding_gallery.models import User

log = logging.getLogger(__name__)


class AuthView:
    def __init__(self, request):
        self.request = request
        self.session = request.session

    @view_config(route_name='login', renderer='../templates/login.jinja2')
    def login(self):
        next_url = self.request.params.get('next', self.request.referrer)
        if not next_url:
            next_url = self.request.route_url('show_photos')
        message = ''
        login = ''
        if self.request.method == "POST":
            login = self.request.POST['login']
            password = self.request.POST['password']
            user = self.request.dbsession.query(
                User).filter_by(name=login).first()
            if user is not None and user.check_password(password):
                headers = remember(self.request, user.id)
                return HTTPFound(location=next_url, headers=headers)
            self.session.flash(
                'Failed login', queue='error')

        return dict(
            url=self.request.route_url('login'),
            next_url=next_url,
            login=login,
        )

    @view_config(route_name='logout', permission='registered')
    def logout(self):
        log.debug("logout")
        headers = forget(self.request)
        next_url = self.request.route_url('show_photos')
        return HTTPFound(location=next_url, headers=headers)

    @forbidden_view_config()
    def forbidden_view(self):
        next_url = self.request.route_url(
            'login', _query={'next': self.request.url})
        return HTTPFound(location=next_url)
