from logging.config import dictConfig
from database import db, app, my_logging_config, run_run_with_debug
from org.woehlke.covid19.who.who_service import WhoService
from org.woehlke.covid19.europe.europe_service import EuropeService
from org.woehlke.covid19.vaccination.vaccination_service import VaccinationService
from org.woehlke.covid19.admin.admin_service import AdminService

drop_and_create_data_again = True

who_service = None
europe_service = None
vaccination_service = None
admin_service = None

#################################################################################################################
#
# MAIN
#
#################################################################################################################
if __name__ == '__main__':
    dictConfig(my_logging_config)
    db.create_all()
    who_service = WhoService(db)
    europe_service = EuropeService(db)
    vaccination_service = VaccinationService(db)
    admin_service = AdminService(db)
    app.run(debug=run_run_with_debug)
