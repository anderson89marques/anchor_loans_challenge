from os.path import basename

from paginate import Page
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from wedding_gallery.models import Like, Photo
from wedding_gallery.s3 import S3Sevice

FILE_FORMATS = ('jpeg', 'jpg', 'png', 'bmp')


class PhotoView:
    def __init__(self, request):
        self.request = request
        self.session = request.session

    @view_config(route_name='upload_photo',
                 renderer='../templates/upload.jinja2', request_method='GET', permission='registered')
    def create(self):
        return {'project': 'weding_gallery'}

    @view_config(route_name='save_photo', request_method='POST', permission='registered')
    def save(self):
        # make sure that filename not contain full path
        filename = basename(self.request.POST['photo'].filename)
        format_ok = self.check_file_format(filename)

        if not format_ok:
            self.session.flash("Photo format is invalid.", queue='error')
            return HTTPFound(location='/upload')

        input_file = self.request.POST['photo'].file
        description = self.request.POST['description']
        u2id = S3Sevice.save(input_file, filename)
        photo = Photo(name=filename, uuid=str(u2id),
                      description=description, total_likes=0)
        photo.creator = self.request.user
        self.request.dbsession.add(photo)
        self.session.flash(
            f"Photo {filename} waiting approvement.", queue='success')
        return HTTPFound(location='/upload')

    @view_config(route_name='show_photos', request_method='GET', permission='registered')
    def show_photos(self):
        return HTTPFound('/photos/1')

    @view_config(route_name='photos',
                 renderer='../templates/home.jinja2', request_method='GET', permission='registered')
    def photos(self):
        dbsession = self.request.dbsession
        query = dbsession.query(Photo).filter_by(is_approved=True).all()
        photos = Page(query, page=int(self.request.matchdict["page"]),
                      items_per_page=3,
                      item_count=len(query))

        return {"photos": photos}

    @view_config(route_name='approve_photos', request_method='GET', permission='admin')
    def show_photos_tobe_approved(self):
        return HTTPFound('/approve_photos/1')

    @view_config(route_name='tobe_approve_photos',
                 renderer='../templates/approve.jinja2', request_method='GET', permission='admin')
    def photos_tobe_approved(self):
        dbsession = self.request.dbsession
        query = dbsession.query(Photo).filter_by(is_approved=False).all()
        photos = Page(query, page=int(self.request.matchdict["page"]),
                      items_per_page=3,
                      item_count=len(query))
        return {"photos": photos}

    @view_config(route_name='approve_photos',
                 request_method='POST', permission='admin')
    def approve_photo(self):
        photo_id = self.request.POST['photo_id']
        photo = self.request.dbsession.query(
            Photo).filter_by(id=photo_id).first()
        photo.is_approved = True
        self.request.dbsession.add(photo)
        self.session.flash(
            f"Photo approved successfully.", queue='success')
        return HTTPFound(location='/approve_photos')

    @view_config(route_name='likes', request_method='POST', renderer='json', permission='admin')
    def likes(self):
        _id = int(self.request.POST['_id'])
        like = bool(int(self.request.POST['like']))
        if like:
            photo = self.request.dbsession.query(
                Photo).filter_by(id=_id).first()
            like = Like(photo=photo, user=self.request.user)
            self.request.dbsession.add(like)
        else:
            like = self.request.dbsession.query(Like).filter_by(
                photo_id=_id, user_id=self.request.user.id).first()
            self.request.dbsession.delete(like)
        total_likes = self.request.dbsession.query(Like).filter_by(
            photo_id=_id).count()
        return {'total_likes': total_likes}

    def check_file_format(self, filename):
        filename_splitted = filename.split('.')
        if len(filename_splitted) == 2 and filename_splitted[1].lower() in FILE_FORMATS:
            return True
        return False
