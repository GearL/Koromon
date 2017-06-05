from sqlalchemy.exc import IntegrityError

from koromon.exts.database import db


class Base(db.Model):
    __abstract__ = True

    @classmethod
    def paginate(cls, page, per_page=20, error_out=True, order_by=None,
                 filters=[], with_deleted=False):
        """A proxy method to return `per_page` items from page `page`.
        If there is `state` attribute in class and `with_deleted` is `False`
        it will filter out which was `state != 'deleted'`.
        If items were not found it will abort with 404.
        Example::
            User(BaseModel):
                id = BaseModel.Column(BaseModel.Integer, primary_key=True)
                name = BaseModel.Column(BaseModel.String(20))
            User.paginate(page=1, per_page=3)
        Returns an :class:`Pagination` object.
        :param order_by: sort by this param
        :param page: Page to show.
        :param per_page: Sepcify how many items in a page.
        :param error_out: If `False`, disable abort with 404.
        :param filters: A list that the query wile filter.
        :param with_deleted: If True, it will not filter `state != 'deleted'`
        """
        query = cls.query

        if hasattr(cls, 'state') and not with_deleted:
            query = query.filter(cls.state != 'deleted')

        for filte in filters:
            query = query.filter(filte)

        if order_by is not None:
            query = query.order_by(order_by)

        pagination = query.paginate(
            page=page,
            per_page=per_page,
            error_out=error_out
        )

        return pagination

    def save(self, commit=True):
        """Proxy method of saving object to database"""
        db.session.add(self)
        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def update(self, form_data, commit=True):
        """Edit object from `form_data`.
        :param form_data: Data to save in object.
        :param commit: If `commit` is `True`
                       it will commit to database immediately
                       after editing object.
        """
        for key, value in form_data.iteritems():
            setattr(self, key, value)

        db.session.add(self)

        if commit:
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def delete(self, commit=True):
        """Delete object from database.
        :param commit: Commit to database immediately
        """
        if hasattr(self, 'deleted'):
            self.deleted = True
        else:
            db.session.delete(self)

        if commit:
            db.session.commit()
