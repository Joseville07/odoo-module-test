from odoo import models, fields

class EstatePropertyTags(models.Model):
    _name = "estate_property_tags"
    _description = "Property Tags"
    
    _sql_constraints = [("name_uniq", "UNIQUE(name)", "A tag with this name already exists")]
    
    name = fields.Char(required=True)
    