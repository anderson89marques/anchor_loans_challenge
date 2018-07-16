"""Module that process data about photo model"""

from os.path import basename

from paginate import Page
from pyramid.httpexceptions import HTTPFound
from pyramid.response import Response
from pyramid.view import view_config

from wedding_gallery.models import Like, Photo
from wedding_gallery.services import PhotoService

FILE_FORMATS = ('jpeg', 'jpg', 'png', 'bmp')


class PhotoView:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        self.db = request.dbsession
        self.photo_service = PhotoService(request.dbsession)

    @view_config(route_name='upload_photo',
                 renderer='../templates/upload.jinja2', request_method='GET', permission='registered')
    def create(self):
        return {'project': 'weding_gallery'}

    @view_config(route_name='save_photo', request_method='POST', permission='registered')
    def save(self):
        """Save photo data that must be saved in database and amazon s3"""
        # make sure that filename not contain full path
        filename = basename(self.request.POST['photo'].filename)
        format_ok = self.check_file_format(filename)

        if not format_ok:
            self.session.flash("Photo format is invalid.", queue='error')
            return HTTPFound(location='/upload')

        self.photo_service.save(self.request.POST, self.request.user)
        self.session.flash(
            f"Photo {filename} waiting approvement.", queue='success')
        return HTTPFound(location='/upload')

    @view_config(route_name='show_photos', request_method='GET', permission='registered')
    def show_photos(self):
        return HTTPFound('/photos/1')

    @view_config(route_name='photos',
                 renderer='../templates/home.jinja2', request_method='GET', permission='registered')
    def photos(self):
        query = self.photo_service.approved_photos()
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
        """Return paginated unapproved photos"""
        query = self.photo_service.unapproved_photos()
        photos = Page(query, page=int(self.request.matchdict["page"]),
                      items_per_page=3,
                      item_count=len(query))
        return {"photos": photos}

    @view_config(route_name='approve_photos',
                 request_method='POST', permission='admin')
    def approve_photo(self):
        """Photo is approved status must be updated to True"""
        photo_id = self.request.POST['photo_id']
        self.photo_service.approve_photo(photo_id)
        self.session.flash(
            f"Photo approved successfully.", queue='success')
        return HTTPFound(location='/approve_photos')

    @view_config(route_name='likes', request_method='POST', renderer='json', permission='registered')
    def likes(self):
        """Like and unlike operation"""
        _id = int(self.request.POST['_id'])
        like = bool(int(self.request.POST['like']))
        if like:
            self.photo_service.like(_id, self.request.user)
        else:
            self.photo_service.unlike(_id, self.request.user)

        total_likes = self.db.query(Like).filter_by(
            photo_id=_id).count()
        print(f"TOTAL: {total_likes}")
        return {'total_likes': total_likes}

    def check_file_format(self, filename):
        """Check if file is at allowed formats."""
        filename_splitted = filename.split('.')
        if len(filename_splitted) == 2 and filename_splitted[1].lower() in FILE_FORMATS:
            return True
        return False
