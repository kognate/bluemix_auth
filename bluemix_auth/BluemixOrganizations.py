from bluemix_auth import BluemixAuth
import requests


class BluemixOrganizations(BluemixAuth):

    def __init__(self, username, password):
        super().__init__(username, password)

    def list_bluemix_organizations(self, next_page=None):
        if self.authentication_information is None:
            self.bluemix_login()

        org_url = '{0}/v2/organizations'.format(self.api)
        if next_page is not None:
            org_url = '{0}{1}'.format(self.api, next_page)

        token = self.authentication_information['access_token']
        headers = {'Authorization' :
                       'bearer {0}'.format(token)}
        response = requests.get(org_url,headers=headers)
        response.raise_for_status()
        return response.json()

    def list_spaces_in_organization(self,
                                    organization_guid=None,
                                    next_page=None):
        if self.authentication_information is None:
            self.bluemix_login()

        space_url = '{0}/v2/organizations/{1}/spaces'.format(self.api,
                                                             organization_guid)
        if next_page is not None:
            space_url = '{0}{1}'.format(self.api, next_page)

        token = self.authentication_information['access_token']
        headers = {'Authorization':
                       'bearer {0}'.format(token)}
        response = requests.get(space_url, headers=headers)
        response.raise_for_status()
        return response.json()