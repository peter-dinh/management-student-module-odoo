# -*- coding: utf-8 -*-
from odoo import http

class Qlsv(http.Controller):
    @http.route('/qlsv/qlsv/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/qlsv/qlsv/objects/', auth='public')
    def list(self, **kw):
        return http.request.render('qlsv.listing', {
            'root': '/qlsv/qlsv',
            'objects': http.request.env['qlsv.sinh_vien'].search([]),
        })

    @http.route('/qlsv/qlsv/objects/<model("qlsv.sinh_vien"):obj>/', auth='public')
    def object(self, obj, **kw):
        return http.request.render('qlsv.object', {
            'object': obj
        })