# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import exceptions
import logging

_logger = logging.getLogger(__name__)

class khoa(models.Model):
    _name = 'qlsv.khoa'
    _rec_name = 'ten_khoa'

    ma_khoa = fields.Char('Mã khoa')
    ten_khoa = fields.Char('Tên khoa')
    so_nam_toi_thieu_tot_nghiep = fields.Integer('Số năm tối thiểu tốt nghiệp')
    

class mon_hoc(models.Model):
    _name = 'qlsv.mon_hoc' 
    _rec_name = 'ten_mon_hoc'

    ma_mon_hoc = fields.Char('Mã môn học', compute='get_ma_mon_hoc')
    ten_mon_hoc = fields.Char('Tên môn học')
    ma_khoa = fields.Many2one('qlsv.khoa', required=True)
    he_so_diem_qua_trinh = fields.Integer(string='Hệ số quá trình')
    he_so_diem_thi = fields.Integer(string='Hệ số thi')
    hocky = fields.Char('Học kỳ')
    so_tin_chi = fields.Integer('Số tín chỉ')

    @api.multi
    def get_ma_mon_hoc(self):
        for item in self:
            item.ma_mon_hoc = 'mon hoc ' + str(item.id)

class diem(models.Model):
    _name = 'qlsv.diem'
    _rec_name = 'ma_sv'

    ma_mon_hoc = fields.Many2one('qlsv.mon_hoc', string="Môn học", required=True)
    ma_sv = fields.Many2one('qlsv.sinh_vien', string="Sinh viên", required=True)
    diem_qua_trinh = fields.Float('Điểm quá trình')
    diem_thi = fields.Float('Điểm thi')
    tong_diem = fields.Float(string='Tổng điểm', compute='_tinh_tong_diem')
    xep_loai = fields.Selection(
            selection=[('1', 'A'), ('2', 'B'), ('3','C'), ('4', 'D'), ('5', 'F'), ('6', 'Nope')],
            string = 'Xếp loại',
            required=True, 
            compute='_danh_gia_xep_loai'
        )

    def danh_gia(self, diem):
        if diem < 0:
            return '6'
        elif diem >= 0 and diem < 4.0:
            return '5'
        elif diem >= 4.0 and diem < 5.5:
            return '4'
        elif diem >= 5.5 and diem < 7.0:
            return '3'
        elif diem >= 7.0 and diem < 8.5:
            return '2'
        else:
            return '1'

    @api.depends('diem_thi', 'diem_qua_trinh')
    @api.multi
    def _tinh_tong_diem(self):
        for item in self:
            mon_hoc = item.env['qlsv.mon_hoc'].search([('id', '=', item.ma_mon_hoc.id)])
            tong = (item.diem_qua_trinh * mon_hoc.he_so_diem_qua_trinh + item.diem_thi * mon_hoc.he_so_diem_thi)/100
            item.tong_diem = tong

    @api.depends('tong_diem')
    @api.multi
    def _danh_gia_xep_loai(self):
        for item in self:
            loai_diem = item.danh_gia(item.tong_diem)
            #_logger.debug(loai_diem)
            item.xep_loai = loai_diem


class sinh_vien(models.Model):
    _name = 'qlsv.sinh_vien'
    _rec_name = 'ten_sinh_vien'

    ma_sinh_vien = fields.Char('Mã sinh viên')
    ten_sinh_vien = fields.Char('Tên sinh viên')
    hinh_anh = fields.Binary('Hình ảnh')
    khoa = fields.Many2one('qlsv.khoa',required=True, string='Khoa')
    lop = fields.Char('Lớp')
    nam_nhap_hoc = fields.Char(string='Năm nhập học')
    
    

class thong_tin_sinh_vien(models.Model):
    _name = 'qlsv.thong_tin_sinh_vien'
    _inherit = ['qlsv.sinh_vien', 'mail.thread']


    danh_sach_diem = fields.One2many('qlsv.diem', 'id', string='Danh sách điểm')
    nam_tot_nghiep_du_kien = fields.Char(string="Năm tốt nghiệp", compute='get_nam_tot_nghiep_du_kien')
    tong_so_tin_chi_hoan_thanh = fields.Integer('Tổng số tín chỉ', compute='_cap_nhat_so_tin_chi')

    
    @api.depends('khoa', 'nam_nhap_hoc')
    @api.multi
    def get_nam_tot_nghiep_du_kien(self):
        for item in self:
            if item.khoa == False:
                item.nam_tot_nghiep_du_kien = 'Nope'
            else:
                so_nam = item.env['qlsv.khoa'].search([('id', '=', item.khoa.id)]).so_nam_toi_thieu_tot_nghiep
                item.nam_tot_nghiep_du_kien = str(int(item.nam_nhap_hoc) + so_nam)

    @api.multi
    def _cap_nhat_so_tin_chi(self):
        """
            Cập nhật số tín chỉ thông qua danh sách điểm
        """
        for item in self:
            tong_tin = 0
            for item_diem in item.danh_sach_diem:
                if int(item_diem.xep_loai) < 5:
                    mon_hoc = item_diem.env['qlsv.mon_hoc'].search([('id', '=', item_diem.ma_mon_hoc.id)])
                    if mon_hoc.ma_khoa.id == item.khoa.id: 
                        tong_tin = tong_tin + mon_hoc.so_tin_chi
            item.tong_so_tin_chi_hoan_thanh = tong_tin
    


    
    