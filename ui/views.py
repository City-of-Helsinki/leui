import requests
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"

    def get_le_token(self):
        LE_CLIENT_ID = 'NWOWjp8ik6YuvyGHSX26BgkL34FBKvQyHuSWlaSM'
        if not self.request.user.is_authenticated():
            return None
        token = self.request.user.socialaccount_set\
            .get(provider='helsinki').socialtoken_set.first()
        headers = {'Authorization': 'Bearer %s' % token.token}
        params = {'target_app': LE_CLIENT_ID}
        resp = requests.get('https://api.hel.fi/sso/jwt-token/',
                            headers=headers, params=params)
        if resp.status_code != 200:
            raise Exception('JWT token request returned %d' % resp.status_code)
        return resp.json()['token']

    def get_context_data(self, **kwargs):
        ret = super(HomeView, self).get_context_data(**kwargs)
        ret['jwt_token'] = self.get_le_token()
        return ret
