import os
import csv
import psycopg2

from database import db, app
from covid19.blueprints.rki_vaccination.rki_vaccination_model_import import RkiVaccinationImport
from covid19.blueprints.application.application_service_config import ApplicationServiceConfig


class RkiVaccinationServiceImport:
    def __init__(self, database, config: ApplicationServiceConfig):
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Import [init]")
        app.logger.debug("------------------------------------------------------------")
        self.__database = database
        self.cfg = config
        app.logger.debug("------------------------------------------------------------")
        app.logger.debug(" Vaccination Service Import [ready]")

    def __int(self, input_string: str):
        if input_string == '#REF!':
            return 0
        else:
            return int(input_string)

    def import_file(self):
        src_cvsfile_name = self.cfg.data_path+os.sep+self.cfg.cvsfile_name
        app.logger.info(" import Vaccination [begin]")
        app.logger.info("------------------------------------------------------------")
        app.logger.info(" import into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
        app.logger.info("------------------------------------------------------------")
        try:
            RkiVaccinationImport.remove_all()
            k = 0
            with open(src_cvsfile_name, newline='\n') as csv_file:
                file_reader = csv.DictReader(csv_file, delimiter='\t', quotechar='"')
                for row in file_reader:
                    o = RkiVaccinationImport(
                        datum=row['date'],
                        dosen_kumulativ=self.__int(row['dosen_kumulativ']),
                        dosen_differenz_zum_vortag=self.__int(row['dosen_differenz_zum_vortag']),
                        dosen_biontech_kumulativ=self.__int(row['dosen_biontech_kumulativ']),
                        dosen_moderna_kumulativ=self.__int(row['dosen_moderna_kumulativ']),
                        personen_erst_kumulativ=self.__int(row['personen_erst_kumulativ']),
                        personen_voll_kumulativ=self.__int(row['personen_voll_kumulativ']),
                        impf_quote_erst=float(row['impf_quote_erst']),
                        impf_quote_voll=float(row['impf_quote_voll']),
                        indikation_alter_dosen=self.__int(row['indikation_alter_dosen']),
                        indikation_beruf_dosen=self.__int(row['indikation_beruf_dosen']),
                        indikation_medizinisch_dosen=self.__int(row['indikation_medizinisch_dosen']),
                        indikation_pflegeheim_dosen=self.__int(row['indikation_pflegeheim_dosen']),
                        indikation_alter_erst=self.__int(row['indikation_alter_erst']),
                        indikation_beruf_erst=self.__int(row['indikation_beruf_erst']),
                        indikation_medizinisch_erst=self.__int(row['indikation_medizinisch_erst']),
                        indikation_pflegeheim_erst=self.__int(row['indikation_pflegeheim_erst']),
                        indikation_alter_voll=self.__int(row['indikation_alter_voll']),
                        indikation_beruf_voll=self.__int(row['indikation_beruf_voll']),
                        indikation_medizinisch_voll=self.__int(row['indikation_medizinisch_voll']),
                        indikation_pflegeheim_voll=self.__int(row['indikation_pflegeheim_voll'])
                    )
                    db.session.add(o)
                    k += 1
                    if (k % 100) == 0:
                        db.session.commit()
                        app.logger.info(" import Vaccination  ... " + str(k) + " rows")
            db.session.commit()
            app.logger.info(" import Vaccination  ... " + str(k) + " rows total")
        except KeyError as error:
            app.logger.warning("WARN: import Vaccination [begin]")
            app.logger.warning(":::"+str(error)+":::")
            for item_key, item_value in row.items():
                app.logger.warning(item_key+" : "+item_value)
            app.logger.warning("WARN: import Vaccination [end]")
        except (Exception, psycopg2.DatabaseError) as error:
            app.logger.warning("WARN: import Vaccination [begin]")
            app.logger.warning(error)
            app.logger.warning("WARN: import Vaccination [end]")
        finally:
            app.logger.info("")
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" imported into TABLE: "+self.cfg.tablename+" from "+self.cfg.cvsfile_path)
            app.logger.info("------------------------------------------------------------")
            app.logger.info(" import Vaccination [done]")
        return self
