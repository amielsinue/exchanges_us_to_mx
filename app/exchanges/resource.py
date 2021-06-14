from app.exchanges.controller import ExchangesController
from app.libs.auth import requires_auth
from app.libs.resource import BaseResource


class Exchanges(BaseResource):

    @requires_auth
    def get(self):
        data = ExchangesController.get_all()
        return {"rates": data}
