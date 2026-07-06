from odoo import http
from odoo.http import request

class TimeAccessPortal(http.Controller):

    @http.route('/index/profile', type='http', auth='user', website=True)
    def index_f(self, **kw):
        partner = request.env.user.partner_id.sudo()
        # One-time success message
        profile_saved = request.session.pop('profile_saved', False)

        return request.render('time_access_portal.profile_page', {
            'active_menu': 'profile',
            'partner': partner,
            'profile_saved': profile_saved,
        })

    @http.route('/index/profile/save', type='http', auth='user', website=True, methods=['POST'], csrf=True)
    def profile(self, **kw):
        partner = request.env.user.partner_id.sudo()
        vals = {
            'name': kw.get('name') or partner.name,
            'email': kw.get('email') or False,
            'mobile': kw.get('mobile') or False,
            'street': kw.get('street') or False,
        }

        # Set success message flag
        request.session['profile_saved'] = True

        partner.write(vals)
        return request.redirect('/index/profile')