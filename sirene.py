from api_insee import ApiInsee
from api_insee.criteria import Field ,Periodic
import os
from dotenv.main import load_dotenv
import pymongo
import schedule
from datetime import datetime
from typing import List, Dict
import logging

load_dotenv()

# api key
KEY = os.getenv("KEY", "")
SECRET = os.getenv("SECRET", "")
USERMONGO = os.getenv("USERMONGO", "")
PASSWDMONGO = os.getenv("PASSWDMONGO", "")

def insert_mongo(societies: List[Dict[str, str]]) -> None:
    """ insert societies in mongodb

    Args:
        societies (List): list of dict societies to insert
    """
    myclient = pymongo.MongoClient("mongodb://localhost:27017/",
        username=USERMONGO,
        password=PASSWDMONGO)
    db = myclient.database
    collection = db.societies
    collection.insert_many(societies)


def siren_request(api: ApiInsee) -> None:
    """ request 100 first societies with NAF code 62.01Z on ApiInsee

    Args:
        api (ApiInsee): Insee Api
    """
    request = api.siret(
        q=Periodic(Field('activitePrincipaleEtablissement','62.01Z'))
    )

    # list 100 first societies
    for (page_index, page_result) in enumerate(request.pages(nombre=100)):
        society_list = page_result['etablissements']
        break

    # parse societies to insert
    societies = []
    for society in society_list:
        societies.append({
            'siren': society['siren'],
            'Prenom': society['uniteLegale']['prenom1UniteLegale'],
            'Nom': society['uniteLegale']['nomUniteLegale'],
            'DateDeCreation': society['dateCreationEtablissement'],
            'DenominationSociale': society['uniteLegale']['denominationUniteLegale'],
            'CodeNAF': society['uniteLegale']['nomenclatureActivitePrincipaleUniteLegale'],
            'ActivitePrincipaleUniteLegale': society['uniteLegale']['activitePrincipaleUniteLegale'],
            'DerniereDateDeSynchronisationDeLAPI': str(datetime.now())
        })
    
    # insert data
    insert_mongo(societies)

    # logger
    logging.basicConfig(format='%(asctime)s %(message)s',level=logging.INFO)
    logging.info(f'updated db : {len(societies)} first societies')


if __name__ == '__main__':
    api = ApiInsee(
        key = KEY,
        secret = SECRET
    )

    # schedule every day at 10am UTC
    schedule.every().day.at("10:00").do(siren_request, api)

    while True:
        schedule.run_pending()
