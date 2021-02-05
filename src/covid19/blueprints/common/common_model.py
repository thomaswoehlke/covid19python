from sqlalchemy import and_, func
from datetime import date
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload


class CommonDateReported(db.Model):
    __tablename__ = 'common_date_reported'
    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False, unique=True)
    year_week = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)

    day_of_year = db.Column(db.Integer, nullable=True)
    year_day_of_year = db.Column(db.String(255), nullable=True, unique=True)

    def __str__(self):
        result = ""
        if self.day_of_month < 10:
            result += "0" + str(self.day_of_month)
        else:
            result += "" + str(self.day_of_month)
        if self.month < 10:
            result += ".0" + str(self.month)
        else:
            result += "." + str(self.month)
        result += "." + str(self.year)
        return result

    def get_name_for_weekday(self):
        return self.get_names_for_weekday()[self.day_of_week]

    @classmethod
    def get_names_for_weekday(cls):
        return {1: "Montag", 2: "Dienstag", 3: "Mittwoch", 4: "Donnerstag", 5: "Freitag", 6: "Samstag",
                             7: "Sonntag"}

    @classmethod
    def create_new_object_factory(cls, my_date_rep):
        my_datum = date.fromisoformat(my_date_rep)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        if week_number < 10:
            my_year_week = "" + str(my_iso_year) + "-0"+str(week_number)
        else:
            my_year_week = "" + str(my_iso_year) + "-"+str(week_number)
        return CommonDateReported(
            date_reported=my_date_rep,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week
        )

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.date_reported.desc())\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_dict(cls):
        dates_reported = {}
        for my_date_reported in cls.get_all():
            dates_reported[my_date_reported.date_reported] = my_date_reported
        return dates_reported

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_date_reported(cls, i_date_reported):
        return db.session.query(cls)\
            .filter(cls.date_reported == i_date_reported)\
            .one_or_none()

    @classmethod
    def get_by_date_reported(cls, i_date_reported):
        return db.session.query(cls)\
            .filter(cls.date_reported == i_date_reported)\
            .one()

    @classmethod
    def find_by_year_week(cls, year_week):
        return db.session.query(cls).filter(cls.year_week == year_week).one()


class CommonRegion(db.Model):
    __tablename__ = 'common_region'
    discriminator = db.Column('type', db.String(50))
    __mapper_args__ = {'polymorphic_on': discriminator}

    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), unique=True)

    @classmethod
    def remove_all(cls):
        # TODO: SQLalchemy instead of SQL
        db.session.execute("delete from " + cls.__tablename__)
        db.session.commit()
        return None

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls)\
            .order_by(cls.region)\
            .paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all_as_dict(cls):
        regions = {}
        for my_region in cls.get_all():
            regions[my_region.region] = my_region
        return regions

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_region(cls, i_who_region):
        return db.session.query(cls)\
            .filter(cls.region == i_who_region)\
            .one_or_none()
