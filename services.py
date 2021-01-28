from database import db

from app.oodm.common.common_service import CommonService
from app.oodm.who.who_service import WhoService
from app.oodm.europe.europe_service import EuropeService
from app.oodm.rki.rki_service import RkiService
from app.oodm.vaccination.vaccination_service import VaccinationService
from app.oodm.admin.admin_service import AdminService

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
