from database import db

from covid19.blueprints.common.common_service import CommonService
from covid19.blueprints.who.who_service import WhoService
from covid19.blueprints.europe.europe_service import EuropeService
from covid19.blueprints.rki_bundeslaender.rki_service import RkiBundeslaenderService
from covid19.blueprints.rki_landkreise.rki_service import RkiLandkreiseService
from covid19.blueprints.vaccination.vaccination_service import VaccinationService
from covid19.blueprints.admin.admin_service import AdminService

############################################################################################
#
# Services
#
common_service = CommonService(db)
who_service = WhoService(db)
europe_service = EuropeService(db)
rki_service_bundeslaender = RkiBundeslaenderService(db)
rki_service_landkreise = RkiLandkreiseService(db)
vaccination_service = VaccinationService(db)
admin_service = AdminService(db)
db.create_all()
