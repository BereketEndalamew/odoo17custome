from odoo import models, fields, api

class CountryState(models.Model):
    _inherit = "res.country.state"

    city_ids = fields.One2many('res.city', 'state_id', string="Cities")

class City(models.Model):
    _name = "res.city"
    _description = "City"

    name = fields.Char(string="City Name", required=True)
    state_id = fields.Many2one('res.country.state', string="State", required=True)
    woreda_ids = fields.One2many('res.woreda', 'city_id', string="Woredas")

class Woreda(models.Model):
    _name = "res.woreda"
    _description = "Woreda"

    name = fields.Char(string="Woreda Name", required=True)
    city_id = fields.Many2one('res.city', string="City", required=True)
    # kebele_ids = fields.One2many('res.kebele', 'woreda_id', string="Kebeles")

# class Kebele(models.Model):
#     _name = "res.kebele"
#     _description = "Kebele"
#
#     name = fields.Char(string="Kebele Name", required=True)
#     woreda_id = fields.Many2one('res.woreda', string="Woreda", required=True)
