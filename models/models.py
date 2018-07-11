# -*- coding: utf-8 -*-

from odoo import models, fields, api

from odoo import exceptions
import logging
import datetime

_logger = logging.getLogger(__name__)

class khoa(models.Model):
    _name = 'qlsv.khoa'
    _rec_name = 'ten_khoa'

    ten_khoa = fields.Char('Tên khoa')
    ma_khoa = fields.Char('Mã khoa')
    so_nam_toi_thieu_tot_nghiep = fields.Integer('Số năm tối thiểu tốt nghiệp')

    _sql_constraints = [
        ('ma_khoa_unique', 'unique (ma_khoa)', 'Ma khoa da ton tai!')
    ]
    
class lop(models.Model):
    _name = 'qlsv.lop'
    _rec_name = 'ten_lop'
    
    ma_lop = fields.Char(string="Ma lop", required=True)
    ten_lop = fields.Char(string="Ten lop", compute="_get_ten_lop")
    ma_khoa = fields.Many2one('qlsv.khoa', required=True)

    _sql_constraints = [
        ('ma_lop_unique', 'unique (ma_lop)', 'Ma lop da ton tai!')
    ]

    @api.depends('ma_khoa', 'ma_lop')
    def _get_ten_lop(self):
        for item in self:
            ma_khoa = item.env['qlsv.khoa'].search([('id', '=', item.ma_khoa.id)]).ma_khoa
            item.ten_lop = str(ma_khoa) + " - " + str(item.ma_lop)


    # @api.multi
    # def _get_ten_lop(self):
    #     for item in self:
    #         ten_khoa_viet_tat = self.env['qlsv.khoa'].search([('id', '=', item.ma_khoa.id)]).ma_khoa
            

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


    _sql_constraints = [
        ('ma_mon_hoc_unique', 'unique (ma_mon_hoc)', 'Ma mon hoc da ton tai!')
    ]


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


class thong_tin_sinh_vien(models.Model):
    _name = 'qlsv.thong_tin_sinh_vien'
    _rec_name = 'ten_sinh_vien'

    ma_sinh_vien = fields.Char('Mã sinh viên', required=True)
    ten_sinh_vien = fields.Char('Tên sinh viên')
    hinh_anh = fields.Binary('Hình ảnh')
    nam_nhap_hoc = fields.Char(string='Năm nhập học', required=True)
    
    _sql_constraints = [
        ('ma_sinh_vien_unique', 'unique (ma_sinh_vien)', 'Ma sinh vien da ton tai!')
    ]


class sinh_vien(models.Model):
    _name = 'qlsv.sinh_vien'
    _inherit = ['qlsv.thong_tin_sinh_vien', 'mail.thread']

    khoa = fields.Many2one('qlsv.khoa',required=True, string='Khoa')
    lop = fields.Many2one('qlsv.lop', required=True)
    danh_sach_diem = fields.One2many('qlsv.diem', 'id', string='Danh sách điểm')
    nam_tot_nghiep_du_kien = fields.Char(string="Năm tốt nghiệp")
    tong_so_tin_chi_hoan_thanh = fields.Integer('Tổng số tín chỉ', compute='_cap_nhat_so_tin_chi')
    nghi_hoc = fields.Boolean(string="Nghi hoc", default=False)

    # @api.multi
    # def _get_ma_sinh_vien(self):
    #     for item in self:
    #         list_khoa = self.
            

    @api.constrains('khoa', 'lop')
    @api.multi
    def _check_lop_in_khoa(self):
        for item in self:
            check_khoa_of_lop = item.env['qlsv.lop'].search([('id', '=', item.lop.id)]).ma_khoa
            if check_khoa_of_lop.id != item.khoa.id:
                raise exceptions.ValidationError("Lop hoc khong phu hop voi khoa!")
            else:
                print('errrr!')

    # @api.constrains('nam_nhap_hoc')
    # @api.multi
    # def rule_nam_nhap_hoc(self):
    #     for item in self:
    #         now_year = datetime.date.today().year
    #         try:
    #             if int(item.nam_nhap_hoc) < 1900:
    #                 raise exceptions.ValidationError('Nam nhap hoc khong duoc truoc nam 1900')
    #             elif int(item.nam_nhap_hoc) > now_year:
    #                 raise exceptions.ValidationError('Nam nhap hoc khong duoc lon hon nam nay!')
    #         except:
    #             item.nam_nhap_hoc = False
    #             raise exceptions.ValidationError('Nam nhap hoc khong phai la so!')

    @api.onchange('khoa', 'nam_nhap_hoc')
    @api.multi
    def get_nam_tot_nghiep_du_kien(self):
        for item in self:
            now_year = datetime.date.today().year
            if item.nam_nhap_hoc != False:
                try:
                    nam_nhap_hoc = int(item.nam_nhap_hoc)
                except ValueError:
                    raise exceptions.ValidationError('Nam nhap hoc khong phai la so!')

                if nam_nhap_hoc < 1900:
                    raise exceptions.ValidationError('Nam nhap hoc khong duoc truoc nam 1900')
                elif nam_nhap_hoc > now_year:
                    raise exceptions.ValidationError('Nam nhap hoc khong duoc lon hon nam nay!')
                if item.khoa == False:
                    item.nam_tot_nghiep_du_kien = 'Nope'
                elif item.nam_nhap_hoc == False:
                    item.nam_tot_nghiep_du_kien == 'Nope'
                else:
                    so_nam = item.env['qlsv.khoa'].search([('id', '=', item.khoa.id)]).so_nam_toi_thieu_tot_nghiep
                    item.nam_tot_nghiep_du_kien = str(nam_nhap_hoc + so_nam)


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


class giao_vien(models.Model):
    _name = "qlsv.giao_vien"
    _rec_name = 'ten_giao_vien'

    tai_khoan = fields.Many2one('res.users', string="Tai khoan", required=True)
    ma_giao_vien = fields.Char(string="Ma giao vien")
    ten_giao_vien = fields.Char(string="Ten giao vien")
    ma_khoa = fields.Many2one('qlsv.khoa', required=True)
    lop_chu_nhiem = fields.Many2one('qlsv.lop', reuqired=True)
    
    _sql_constraints = [
        ('ma_giao_vien_unique', 'unique (ma_giao_vien)', 'Ma giao vien da ton tai!')
    ]

    @api.constrains('ma_khoa', 'lop_chu_nhiem')
    @api.multi
    def _check_lop_chu_nhiem_in_khoa(self):
        for item in self:
            check_khoa_of_lop = item.env['qlsv.lop'].search([('id', '=', item.lop_chu_nhiem.id)]).ma_khoa
            if check_khoa_of_lop.id != item.ma_khoa.id:
                raise exceptions.ValidationError("Lop hoc khong phu hop voi khoa!")
            else:
                print('errrr!')

