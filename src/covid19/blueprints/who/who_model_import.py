from database import db, ITEMS_PER_PAGE


class WhoGlobalDataImportTable(db.Model):
    __tablename__ = 'who_global_data_import'

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
            db.session.delete(one).cascade()
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
            .distinct()

    @classmethod
    def get_dates_reported(cls):
        return db.session.query(cls.date_reported)\
            .order_by(cls.date_reported.desc())\
            .distinct()

    @classmethod
    def get_for_one_day(cls, day):
        return db.session.query(cls)\
            .filter(cls.date_reported == day)\
            .order_by(cls.country.asc())\
            .all()

    @classmethod
    def get_new_dates_as_array(cls):
        # TODO: SQLalchemy instead of SQL
        sql_query = """
            select
                date_reported
            from
                who_global_data_import
            where
                date_reported
            not in (
            select
                distinct
                    common_date_reported.date_reported
                from
                    who_global_data
                left join
                    common_date_reported
                on
                    who_global_data.date_reported_id=common_date_reported.id
            )
            group by
                who_global_data_import.date_reported
            order by date_reported desc
            """
        new_dates = []
        for item in db.session.execute(sql_query):
            new_dates.append(item['date_reported'])
        return new_dates

    @classmethod
    def countries(cls):
        sql_query = """
            select distinct 
                who_global_data_import.country_code,
                who_global_data_import.country,
                who_global_data_import.who_region
                from who_global_data_import
            """
        return db.session.execute(sql_query).fetchall()
