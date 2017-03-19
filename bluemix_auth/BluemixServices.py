from bluemix_auth import BluemixAuth
import requests


class BluemixServices(BluemixAuth):
    def __init__(self, username, password):
        super().__init__(username, password)

    def _get_cf_url(self, cf_url):
        if self.authentication_information is None:
            self.bluemix_login()
        token = self.authentication_information['access_token']
        headers = {'Authorization':
                       'bearer {0}'.format(token)}
        response = requests.get(cf_url, headers=headers)
        response.raise_for_status()
        return response.json()

    def list_services(self, next_page=None):
        services_url = '{0}/v2/services'.format(self.api)
        if next_page is not None:
            services_url = '{0}{1}'.format(self.api, next_page)
        return self._get_cf_url(services_url)

    def get_service_detail(self, service_guid=None, next_page=None):
        services_url = '{0}/v2/services/{1}'.format(self.api, service_guid)
        if next_page is not None:
            services_url = '{0}{1}'.format(self.api, next_page)
        return self._get_cf_url(services_url)

    def list_service_instances(self, next_page=None):
        service_instances_url = '{0}/v2/service_instances'.format(self.api)
        if next_page is not None:
            service_instances_url = '{0}{1}'.format(self.api, next_page)
        return self._get_cf_url(service_instances_url)

    def list_service_keys(self, service_instance_guid=None, next_page=None):
        # /v2/service_keys
        service_keys_url = '{0}/v2/service_instances/{1}/service_keys'.format(self.api,service_instance_guid)
        if next_page is not None:
            service_keys_url = '{0}{1}'.format(self.api, next_page)
        return self._get_cf_url(service_keys_url)