# -*- coding: utf-8 -*-

from odoo import models, fields, api, exceptions
import os
from collections import defaultdict
import math

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_compare

class System_Check(models.Model):
    _name = 'system.check'
    _order = 'create_date desc'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    '''
    def create(self, cr, user, vals, context=None):
        if ('name' not in vals) or (vals.get('name')=='Neuer Systemcheck'):
            vals['name'] = self.pool.get('ir.sequence').get(cr, user, 'panel.syscheck.sec')
        new_id = super(System_Check, self).create(cr, user, vals, context)
        return new_id
        '''

    @api.one
    def confirm(self):
        self.write({'state': 'confirmed'})
        self.write({'date_confirmed': fields.Datetime.now()})
        self.write({'confirmed_by': self.env['res.users'].browse(self.env.uid).id})
    
    @api.one
    def done(self):
        self.write({'state': 'done'})
    
    @api.one
    def edit(self):
        self.write({'state': 'draft'})
    
    # General Data
    name = fields.Char(default="Neuer Systemcheck", readonly=True)
    system_type = fields.Many2one('system.check.config', string='Systemkonfiguration', track_visibility='onchange')
    date_confirmed = fields.Datetime('Bestätigt am', readonly=True)
    confirmed_by = fields.Many2one('res.users', string="Bestätigt durch", readonly=True)
    
    #Pretacking Data
    pt_kraft_soll = fields.Float(string="Soll-Kraft", related='system_type.pt_kraft_soll', readonly = True)
    pt_temp_soll = fields.Float(string="Soll-Temperatur", related='system_type.pt_temp_soll', readonly = True)
    pt_zeit_soll = fields.Float(string="Soll-Zeit", related='system_type.pt_zeit_soll', readonly = True)
    pt_force_sys = fields.Float(string="F_sys", related='system_type.pt_force_sys', readonly = True)
    pt_temp_sys = fields.Float(string="Temp_sys", related='system_type.pt_temp_sys', readonly = True)
    
    pt_kraft_ist = fields.Float(string="Ist-Kraft", required = True)
    pt_temp_ist = fields.Float(string="Ist-Temperatur", required = True)
    pt_zeit_ist = fields.Float(string="Ist-Zeit", required = True)
    pt_force_sys_ist = fields.Float(string="Ist F_sys", required = True)
    pt_temp_sys_ist = fields.Float(string="Ist Temp_sys", required = True)

    #Final Bonding Data
    hsb_kraft_soll = fields.Float(string="Soll-Kraft", related='system_type.hsb_kraft_soll', readonly = True)
    hsb_temp_soll = fields.Float(string="Soll-Temperatur", related='system_type.hsb_temp_soll', readonly = True)
    hsb_zeit_soll = fields.Float(string="Soll-Zeit", related='system_type.hsb_zeit_soll', readonly = True)
    hsb_force_sys = fields.Float(string="F_sys", related='system_type.hsb_force_sys', readonly = True)
    hsb_temp_sys = fields.Float(string="Temp_sys", related='system_type.hsb_temp_sys', readonly = True)
    
    hsb_kraft_ist = fields.Float(string="Ist-Kraft", required = True)
    hsb_temp_ist = fields.Float(string="Ist-Temperatur", required = True)
    hsb_zeit_ist = fields.Float(string="Ist-Zeit", required = True)
    hsb_force_sys_ist = fields.Float(string="Ist F_sys", required = True)
    hsb_temp_sys_ist = fields.Float(string="Ist Temp_sys", required = True)
    
    # Bondblock height
    height_bond_block = fields.Float(string="H Bondblock Soll", related='system_type.height_bond_block', readonly = True)
    
    ist_height_bond_block_1 = fields.Float(string="H Bondblock 1", required = True)
    ist_height_bond_block_2 = fields.Float(string="H Bondblock 2", required = True)
    ist_height_bond_block_3 = fields.Float(string="H Bondblock 3", required = True)
    ist_height_bond_block_4 = fields.Float(string="H Bondblock 4", required = True)

    state = fields.Selection([
        ('draft', 'Entwurf'),
        ('confirmed', 'Bestätigt'),
        ('done', 'Abgeschlossen'),
        ('cancel', 'Abgebrochen'),
        ], default='draft', track_visibility="onchange")


class System_Check_Config(models.Model):
    _name = 'system.check.config'
    
    # General Data
    name = fields.Char(sting="Konfigurationsname", default="Neue Konfiguration", Required=True)
    
    #Pretacking Data
    pt_kraft_soll = fields.Float(string="Soll-Kraft", required = True)
    pt_temp_soll = fields.Float(string="Soll-Temperatur", required = True)
    pt_zeit_soll = fields.Float(string="Soll-Zeit", required = True)
    pt_force_sys = fields.Float(string="F_sys", required = True)
    pt_temp_sys = fields.Float(string="Temp_sys", required = True)
    
    #HSB Data
    hsb_kraft_soll = fields.Float(string="Soll-Kraft", required = True)
    hsb_temp_soll = fields.Float(string="Soll-Temperatur", required = True)
    hsb_zeit_soll = fields.Float(string="Soll-Zeit", required = True)
    hsb_force_sys = fields.Float(string="F_sys", required = True)
    hsb_temp_sys = fields.Float(string="Temp_sys", required = True)
    
    # Bondblock height
    height_bond_block = fields.Float(string="H Bondblock", required = True)
