from database import db

from covid19.blueprints.admin.admin_service import AdminService
from covid19.blueprints.common.application_service import CommonService
from covid19.blueprints.ecdc.ecdc_service import EcdcService
from covid19.blueprints.rki_bundeslaender.rki_service import RkiBundeslaenderService
from covid19.blueprints.rki_landkreise.rki_service import RkiLandkreiseService
from covid19.blueprints.rki_vaccination.rki_vaccination_service import VaccinationService
from covid19.blueprints.who.who_service import WhoService


############################################################################################
#
# Services
#
admin_service = AdminService(db)
application_service = CommonService(db)
ecdc_service = EcdcService(db)
rki_service_bundeslaender = RkiBundeslaenderService(db)
rki_service_landkreise = RkiLandkreiseService(db)
rki_vaccination_service = VaccinationService(db)
who_service = WhoService(db)
db.create_all()
