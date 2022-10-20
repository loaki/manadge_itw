from api_insee import ApiInsee
from api_insee.criteria import Field ,Periodic
import os
from dotenv.main import load_dotenv

load_dotenv()

# Discord config
KEY = os.getenv("KEY", "")
SECRET = os.getenv("SECRET", "")

def siren_request(api):
    request = api.siret(
        q=Periodic(Field('activitePrincipaleEtablissement','62.01Z'))
    ).get()

    if request['header']['statut'] == 200:
        print(request['etablissements'][0])

if __name__ == '__main__':
    api = ApiInsee(
        key = KEY,
        secret = SECRET
    )
    siren_request(api)
