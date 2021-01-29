from database import db

from covid19.oodm.common.common_service import CommonService
from covid19.oodm.who.who_service import WhoService
from covid19.oodm.europe.europe_service import EuropeService
from covid19.oodm.rki.rki_service import RkiService
from covid19.oodm.vaccination.vaccination_service import VaccinationService
from covid19.oodm.admin.admin_service import AdminService

############################################################################################
#
# Services
#
common_service = CommonService(db)
who_service = WhoService(db)
europe_service = EuropeService(db)
rki_service = RkiService(db)
vaccination_service = VaccinationService(db)
admin_service = AdminService(db)
db.create_all()
