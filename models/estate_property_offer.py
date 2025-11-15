from odoo import models, fields

class EstatePropertyOffer(models.Model):
    _name = 'estate_property_offer'
    _description = 'Estate Property Offer'

    price = fields.Float(string='Offer Price', required=True)
    status = fields.Selection([
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], string='Status', default='refused', required=True)
    property_id = fields.Many2one(comodel_name="estate_property", string='Property', required=True)
    partner_id = fields.Many2one(comodel_name="res.partner", string='Buyer', required=True)
