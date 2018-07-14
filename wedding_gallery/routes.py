from wedding_gallery.settings import STATIC_URL

def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_static_view(STATIC_URL, 'wedding_gallery:images', cache_max_age=3600)
    config.add_route('upload_photo', '/upload')
    config.add_route('save_photo', '/upload_save')
    config.add_route('show_photos', '/')
    config.add_route('register', '/register')
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')