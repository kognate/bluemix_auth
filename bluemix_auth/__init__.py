import requests

class BluemixAuth:
    def __init__(self,
                 username,
                 password,
                 api='https://api.ng.bluemix.net',
                 ow_api='https://openwhisk.ng.bluemix.net'):
        super()
        self.username = username
        self.password = password
        self.api = api
        self.ow_api = ow_api
        self.authorization_endpoint_url = None
        self.authentication_information = None
        self.openwhisk_keys = None

    def authorization_endpoint(self):
        if self.authorization_endpoint_url is None:
            response = requests.get('{0}/info'.format(self.api))
            response.raise_for_status()
            self.authorization_endpoint_url = "{0}/oauth/token".format(response.json()['authorization_endpoint'])
        return self.authorization_endpoint_url

    def bluemix_login(self):
        form_data = {'grant_type': 'password', 'username': self.username, 'password': self.password}
        headers = {'Accept': 'application/json;charset=utf-8', 'Authorization': 'basic Y2Y6'}
        response = requests.post(self.authorization_endpoint(),
                                 data=form_data,
                                 headers=headers)
        response.raise_for_status()
        self.authentication_information = response.json()

    def openwhisk_key_for_namespace(self,
                                    namespace=None,
                                    organization=None,
                                    space=None):
        if namespace is None:
            if organization is None or space is None:
                raise Exception("Must supply namespace or Org/Space")

        if self.authentication_information is None:
            self.bluemix_login()

        if self.openwhisk_keys is None:
            json_payload = {'accessToken': self.authentication_information['access_token'],
                            'refreshToken': self.authentication_information['refresh_token']}

            response = requests.post("{0}/bluemix/v1/authenticate".format(self.ow_api), json=json_payload)
            self.openwhisk_keys = dict([(x['name'], (x["uuid"], x["key"]))
                                        for x
                                        in response.json()['namespaces']])
        if namespace is None:
            namespace = "{0}_{1}".format(organization, space)
            return self.openwhisk_keys[namespace]
        else:
            return self.openwhisk_keys[namespace]
