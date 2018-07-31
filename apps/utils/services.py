from oauth2client.client import flow_from_clientsecrets
from oauth2client.contrib.django_util.storage import DjangoORMStorage
from oauth2client.contrib import xsrfutil
from googleapiclient.discovery import build
from djftmaps import settings
from ..utils.models import CredentialsModel
import httplib2

FLOW = flow_from_clientsecrets(
    settings.GOOGLE_OAUTH2_CLIENT_SECRETS_JSON,
    scope='https://www.googleapis.com/auth/fusiontables',
    redirect_uri='http://localhost:8000/oauth2callback'
)

class GoogleFlow:
    """ Google flow is used generate authorization url, build credentials and service (in this case fusion tables) """

    def __init__(self):
        self.FLOW = FLOW

    def autorization_url(self, request):
        self.FLOW.params['state'] = xsrfutil.generate_token(
            settings.SECRET_KEY,
            request.user
        )
        return self.FLOW.step1_get_authorize_url()

    def credentials(self, request):
        credential = self.FLOW.step2_exchange(request.REQUEST)
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        storage.put(credential)
        return credential

    def service(self, request):
        storage = DjangoORMStorage(CredentialsModel, 'id', request.user, 'credential')
        credential = storage.get()
        http = credential.authorize(httplib2.http())
        service = build('fusiontables', 'v2', http=http)
        return GoogleFusionTableService(service)


class GoogleFusionTableService:
    """ Google fusion table service to save location records and purge whole table """

    def __init__(self, service):
        self.service = service

    def save_location(self, location):
        sql_query = "INSERT INTO {} (Address, Location) VALUES ('{}', '{},{}')"\
            .format(settings.TABLE_ID, location['address'], location['latitude'], location['longitude'])
        query_statement = self.service.query().sql(sql=sql_query)
        return query_statement.execute()

    def purge_table(self):
        sql_query = "DELETE FROM {}".format(settings.TABLE_ID)
        query_statement = self.service.query().sql(sql=sql_query)
        return query_statement.execute()