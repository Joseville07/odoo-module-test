from odoo import models, fields, api

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
    validity = fields.Integer(string="Validity (Days)", default=7)
    deadline_date = fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date")
    
    @api.depends("validity")
    def _compute_deadline_date(self):
        for offer in self:
            offer.deadline_date = fields.Date.add(offer.create_date or fields.Date.today(), days=offer.validity)
            
    def _inverse_deadline_date(self):
        for offer in self:
            create_date = fields.Date.to_date(offer.create_date)
            offer.validity = (offer.deadline_date - create_date).days
