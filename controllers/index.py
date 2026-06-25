from odoo import http
from odoo.http import request


class TimeAccessPortal(http.Controller):

    @http.route('/index', type='http', auth='user', website=True)
    def index_f(self, **kw):
        return request.render('time_access_portal.index_page', {
            'active_menu': 'products',
        })

