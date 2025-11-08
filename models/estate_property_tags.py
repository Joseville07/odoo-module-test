from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = "estate_property_tags"
    _description = "Property Tags"
    
    name = fields.Char(required=True)
    