"""Bussiness logic for photo models"""
from os.path import basename

from sqlalchemy import desc

from wedding_gallery.models import Like, Photo
from wedding_gallery.services import S3Sevice


class PhotoService:
    def __init__(self, db):
        self.db = db

    def save(self, post_obj, user):
        """Save photo"""
        filename = basename(post_obj['photo'].filename)
        input_file = post_obj['photo'].file
        description = post_obj['description']
        u2id = S3Sevice.save(input_file, filename)
        photo = Photo(name=filename, uuid=str(u2id),
                      description=description, total_likes=0)
        photo.creator = user
        if user.role == "admin":
            photo.is_approved = True
        self.db.add(photo)

    def approved_photos(self):
        """Return approved photos"""
        return self.db.query(Photo).filter(Photo.is_approved == True).order_by(desc(Photo.total_likes)).all()

    def approve_photo(self, photo_id):
        """Update photo status to approved"""
        photo = self.db.query(Photo).filter_by(id=photo_id).first()
        photo.is_approved = True
        self.db.add(photo)

    def unapproved_photos(self):
        """Return unapproved photos"""
        return self.db.query(Photo).filter_by(is_approved=False).all()

    def like(self, photo_id, user):
        """Like photo"""
        photo = self.db.query(Photo).filter_by(id=photo_id).first()
        like = Like(photo=photo, user=user)
        self.db.add(like)
        self.update_total_likes(photo_id, True)

    def unlike(self, photo_id, user):
        """Unlike photo"""
        like = self.db.query(Like).filter_by(photo_id=photo_id,
                                             user_id=user.id).first()
        self.db.delete(like)
        self.update_total_likes(photo_id, False)

    def update_total_likes(self, photo_id, is_like):
        photo = self.db.query(Photo).filter_by(id=photo_id).first()
        if is_like:
            photo.total_likes += 1
        else:
            photo.total_likes -= 1
        self.db.add(photo)
