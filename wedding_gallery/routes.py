from wedding_gallery.settings import STATIC_URL
from wedding_gallery.resource import RootResource

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(STATIC_URL, 'wedding_gallery:images', cache_max_age=3600)
    config.add_route('show_photos', '/')
    config.add_route('upload_photo', '/upload', factory=RootResource)
    config.add_route('save_photo', '/upload_save', factory=RootResource)
    config.add_route('approve_photos', '/approve_photos', factory=RootResource)
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout', factory=RootResource)