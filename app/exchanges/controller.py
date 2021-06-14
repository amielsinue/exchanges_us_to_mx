from libs.diario import parse_today as diario
from libs.fixer import parse_today as fixer
from libs.banxico import parse_today as banxico


class ExchangesController(object):

    @staticmethod
    def get_all():
        diario_datum = diario()
        fixer_datum = fixer()
        banxico_datum = banxico()

        data = {}

        if diario_datum:
            date, value = diario_datum
            data['diario'] = {
                "last_updated": date.isoformat(),
                "value": "{:.4f}".format(value)
            }

        if fixer_datum:
            date, value = fixer_datum
            data['fixer'] = {
                "last_updated": date.isoformat(),
                "value": "{:.4f}".format(value)
            }

        if banxico_datum:
            date, value = banxico_datum
            data['banxico'] = {
                "last_updated": date.isoformat(),
                "value": "{:.4f}".format(value)
            }

        return data