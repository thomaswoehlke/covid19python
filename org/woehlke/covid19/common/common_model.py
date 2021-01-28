from database import db, ITEMS_PER_PAGE, transform_datum


class CommonDatum(db.Model):
    __tablename__ = 'common_datum'

    id = db.Column(db.Integer, primary_key=True)
    date_string = db.Column(db.String(255), nullable=False, unique=True)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year_week = db.Column(db.String(255), nullable=True, unique=True)
    year_day_of_year = db.Column(db.String(255), nullable=True, unique=True)
    year = db.Column(db.Integer, nullable=True)
    month = db.Column(db.Integer, nullable=True)
    day_of_week = db.Column(db.Integer, nullable=True)
    day_of_month = db.Column(db.Integer, nullable=True)
    day_of_year = db.Column(db.Integer, nullable=True)
    week_of_year = db.Column(db.Integer, nullable=True)

    @classmethod
    def create_new_datum_factory(cls, date_string):
        # check date_string syntax
        # load if already exists
        old = db.session.query(cls).filter(cls.date_string == date_string).one_or_none()
        if old is None:
            o = CommonDatum(date_string=date_string, datum=transform_datum(date_string))
            # put year
            # put month
            # put datum
            # day_of_month
            # compute day_of_year
            # compute week_of_year
            # put year_week
            db.session.add(o)
            db.session.commit()
        return o

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.date_string.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_dict(cls):
        common_dates = {}
        for my_common_datum in cls.get_all():
            common_dates[my_common_datum.date_string] = my_common_datum
        return common_dates

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one_or_none()
