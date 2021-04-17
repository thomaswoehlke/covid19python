from database import db, ITEMS_PER_PAGE


class WhoImport(db.Model):
    __tablename__ = 'application__import__who'

    id = db.Column(db.Integer, primary_key=True)
    date_reported = db.Column(db.String(255), nullable=False)
    country_code = db.Column(db.String(255), nullable=False)
    country = db.Column(db.String(255), nullable=False)
    who_region = db.Column(db.String(255), nullable=False)
    new_cases = db.Column(db.String(255), nullable=False)
    cumulative_cases = db.Column(db.String(255), nullable=False)
    new_deaths = db.Column(db.String(255), nullable=False)
    cumulative_deaths = db.Column(db.String(255), nullable=False)

    @classmethod
    def remove_all(cls):
        for one in cls.get_all():
            db.session.delete(one)
        db.session.commit()
        return None

    @classmethod
    def get_all_as_page(cls, page):
        return db.session.query(cls).order_by(
            cls.date_reported.desc(),
            cls.country.asc()
        ).paginate(page, per_page=ITEMS_PER_PAGE)

    @classmethod
    def get_all(cls):
        return db.session.query(cls).order_by(
            cls.date_reported.desc(),
            cls.country.asc()
        ).all()

    @classmethod
    def get_by_id(cls, other_id):
        return db.session.query(cls)\
            .filter(cls.id == other_id)\
            .one()

    @classmethod
    def get_regions(cls):
        return db.session.query(cls.who_region)\
            .order_by(cls.who_region)\
            .distinct().all()

    @classmethod
    def get_dates_reported(cls):
        return db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .distinct().all()

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls)\
            .filter(cls.date_reported == day)\
            .order_by(cls.country.asc())\
            .all()

    @classmethod
    def get_dates_reported_as_array(cls):
        myresultarray = []
        myresultset = db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .group_by(cls.date_reported)\
            .distinct()
        for item, in myresultset:
            pass
        return myresultarray

    @classmethod
    def get_new_dates_as_array(cls):
        # TODO: #83 WhoImport.get_new_dates_as_array() SQLalchemy instead of SQL
        sql_query = """
            select
                distinct 
                    application__import__who.date_reported
                from
                    application__import__who
                where
                    date_reported
                not in (
                    select
                        distinct
                            who_datereported.date_reported
                        from
                            who
                        left join
                            who_datereported
                        on
                            who.date_reported_id=who_datereported.id
                        group by 
                            who_datereported.date_reported
                        order by
                            who_datereported.date_reported desc
                )
                group by
                    application__import__who.date_reported
                order by 
                    application__import__who.date_reported desc
            """
        new_dates = []
        for item in db.session.execute(sql_query):
            new_dates.append(item['date_reported'])
        return new_dates

    @classmethod
    def countries(cls):
        # TODO: #___ WhoImport.countries() SQLalchemy instead of SQL
        sql_query = """
            select distinct 
                application__import__who.country_code,
                application__import__who.country,
                application__import__who.who_region
                from application__import__who
            """
        return db.session.execute(sql_query).fetchall()
