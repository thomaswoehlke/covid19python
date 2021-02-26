from sqlalchemy import and_, func
from datetime import date, datetime, time
from database import db, ITEMS_PER_PAGE
from sqlalchemy.orm import joinedload


class ApplicationDateReported(db.Model):
    __tablename__ = 'application_date_reported'
    __table_args__ = (
        db.UniqueConstraint('date_reported', 'datum', name="uix_application_date_reported"),
    )
    #
    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False, unique=True)
    year_week = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    #day_of_year = db.Column(db.Integer, nullable=True)
    #year_day_of_year = db.Column(db.String(255), nullable=True, unique=True)

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
    def get_datum_parts(cls, my_date_rep: str):
        my_date_parts = my_date_rep.split("-")
        my_year = int(my_date_parts[0])
        my_month = int(my_date_parts[1])
        my_day = int(my_date_parts[2])
        datum_parts = (my_year, my_month, my_day)
        return datum_parts

    @classmethod
    def get_datum(cls, my_year: int, my_month: int, my_day: int):
        my_datum = date(my_year, my_month, my_day)
        return my_datum

    @classmethod
    def get_datum_as_str(cls, my_year: int, my_month: int, my_day: int):
        my_datum_tp_be_stored = str(my_year)
        my_datum_tp_be_stored += "-"
        if my_month < 10:
            my_datum_tp_be_stored += "0"
        my_datum_tp_be_stored += str(my_month)
        my_datum_tp_be_stored += "-"
        if my_day < 10:
            my_datum_tp_be_stored += "0"
        my_datum_tp_be_stored += str(my_day)
        return my_datum_tp_be_stored

    @classmethod
    def my_year_week(cls, my_iso_year: int, week_number: int):
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return my_year_week

    @classmethod
    def create_new_object_factory(cls, my_date_rep: str):
        (my_year, my_month, my_day) = cls.get_datum_parts(my_date_rep)
        date_reported = cls.get_datum_as_str(my_year, my_month, my_day)
        my_datum = cls.get_datum(my_year, my_month, my_day)
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        my_year_week = cls.my_year_week(my_iso_year, week_number)
        return ApplicationDateReported(
            date_reported=date_reported,
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
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page: int):
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
    def get_by_id(cls, other_id: int):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_id(cls, other_id: int):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one_or_none()

    @classmethod
    def get_by_date_reported(cls, p_date_reported: str):
        return db.session.query(cls)\
            .filter(cls.date_reported == p_date_reported)\
            .one()

    @classmethod
    def find_by_date_reported(cls, p_date_reported: str):
        return db.session.query(cls)\
            .filter(cls.date_reported == p_date_reported)\
            .one_or_none()

    @classmethod
    def get_by_year_week(cls, year_week: str):
        return db.session.query(cls)\
            .filter(cls.year_week == year_week)\
            .one()

    @classmethod
    def find_by_year_week(cls, year_week: str):
        return db.session.query(cls)\
            .filter(cls.year_week == year_week)\
            .one_or_none()


class ApplicationRegion(db.Model):
    __tablename__ = 'application_region'
    __table_args__ = (
        db.UniqueConstraint('region', name='uix_application_region'),
    )
    id = db.Column(db.Integer, primary_key=True)
    region = db.Column(db.String(255), nullable=False, unique=True)

    def __str__(self):
        result = " " + self.region + " "
        return result

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all(cls):
        return db.session.query(cls).all()

    @classmethod
    def get_all_as_page(cls, page: int):
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
    def get_by_id(cls, other_id: int):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def find_by_id(cls, other_id: int):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one_or_none()

    @classmethod
    def get_by_region(cls, i_region: str):
        return db.session.query(cls)\
            .filter(cls.region == i_region)\
            .one()

    @classmethod
    def find_by_region(cls, i_region: str):
        return db.session.query(cls)\
            .filter(cls.region == i_region)\
            .one_or_none()


class RkiDateReported(ApplicationDateReported):
    __tablename__ = 'rki_date_reported'
    __mapper_args__ = {
        'concrete': True
    }
    __table_args__ = (
        db.UniqueConstraint('date_reported', 'datum', name="uix_rki_date_reported"),
    )

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False)
    year_week = db.Column(db.String(255), nullable=False)
    datum = db.Column(db.Date, nullable=False, unique=True)
    year = db.Column(db.Integer, nullable=False)
    month = db.Column(db.Integer, nullable=False)
    day_of_month = db.Column(db.Integer, nullable=False)
    day_of_week = db.Column(db.Integer, nullable=False)
    week_of_year = db.Column(db.Integer, nullable=False)
    time_of_date_str = db.Column(db.String(255), nullable=False)
    time_of_date = db.Column(db.Time, nullable=False)
    aktualisierung = db.Column(db.String(255), nullable=False, unique=True)

    @classmethod
    def create_new_object_factory(cls, aktualisierung: str):
        aktualisierung_datetime = datetime.fromtimestamp(aktualisierung)
        my_datum = aktualisierung_datetime.date()
        my_time_of_date = aktualisierung_datetime.time()
        my_date_reported_str = my_datum.isoformat()
        my_time_of_date_str = my_time_of_date.isoformat(timespec='seconds')
        (my_iso_year, week_number, weekday) = my_datum.isocalendar()
        my_year_week = "" + str(my_iso_year)
        if week_number < 10:
            my_year_week += "-0"
        else:
            my_year_week += "-"
        my_year_week += str(week_number)
        return RkiDateReported(
            date_reported=my_date_reported_str,
            datum=my_datum,
            year=my_datum.year,
            month=my_datum.month,
            day_of_month=my_datum.day,
            day_of_week=weekday,
            week_of_year=week_number,
            year_week=my_year_week,
            time_of_date_str=my_time_of_date_str,
            time_of_date=my_time_of_date,
            aktualisierung=aktualisierung
        )

    @classmethod
    def find_by_aktualisierung(cls, aktualisierung_from_import: str):
        return db.session.query(cls) \
                .filter(cls.aktualisierung == aktualisierung_from_import) \
                .one_or_none()
