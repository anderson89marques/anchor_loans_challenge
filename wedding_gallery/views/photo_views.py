from os.path import basename

from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from wedding_gallery.models.photo import Photo
from wedding_gallery.s3 import S3Sevice

FILE_FORMATS = ('jpeg', 'jpg', 'png', 'bmp')


class PhotoView:
    def __init__(self, request):
        self.request = request

    @view_config(route_name='upload_photo',
                 renderer='../templates/upload.jinja2', request_method='GET')
    def create(self):
        return {'project': 'weding_gallery'}

    @view_config(route_name='save_photo', request_method='POST')
    def save(self):
        # make sure that filename not contain full path
        filename = basename(self.request.POST['photo'].filename)

        #checking file format:
        format_ok = self.check_file_format(filename)

        if not format_ok:
            print("Aqui")
            return HTTPFound(location='/upload')

        input_file = self.request.POST['photo'].file
        print(self.request.POST['photo'].filename)
        description = self.request.POST['description']
        u2id = S3Sevice.save(input_file, filename)
        photo = Photo(name=filename, uuid=str(u2id),
                      description=description, likes=0)
        self.request.dbsession.add(photo)
        return HTTPFound(location='/upload')

    @view_config(route_name='show_photo',
                 renderer='../templates/mytemplate.jinja2', request_method='GET')
    def show_photo(self):
        dbsession = self.request.dbsession
        photos = dbsession.query(Photo).all()
        print(f"PHOTOS: {photos[0]}")
        return {"uuid": photos[0].uuid}

    def check_file_format(self, filename):
        filename_splitted = filename.split('.')
        if len(filename_splitted) == 2 and filename_splitted[1].lower() in FILE_FORMATS:
            return True
        return False
