from odoo import models, fields, api, _
from odoo.exceptions import UserError
class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Estate Property"
    _sql_constraints = [
        ("check_expected_price", "CHECK(expected_price > 0)", "The expected price must be greater than 0"),
        ("check_selling_price", "CHECK(selling_price >= 0)", "The selling price cant be less than 0")
    ]
    
    
    
    
    
    
    name = fields.Char(string="Property Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    active = fields.Boolean(default=True)
    state = fields.Selection([
                              ('new', 'New'),
                              ('offer_received', 'Offer Received'),
                              ('offer_accepted', 'Offer Accepted'),
                              ('sold', 'Sold'),
                              ('canceled', 'Canceled')
                              ], string="Status", copy=False, required=True, default='new')
    property_type_id = fields.Many2one(comodel_name="estate_property_type")
    property_tags_id = fields.Many2many(comodel_name="estate_property_tags")
    date_availability = fields.Date(default= lambda self: fields.Date.add(fields.Date.today(), months=3))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(selection=[
                                                    ('nort', 'Nort'),
                                                    ('south', 'South'),
                                                    ('east', 'East'),
                                                    ('west', 'West')
                                                    ])
    best_offer = fields.Float(compute="_compute_best_offer")
    total_area = fields.Float(compute="_compute_total_area")
    offer_ids = fields.One2many(comodel_name="estate_property_offer", inverse_name="property_id")
    buyer_id = fields.Many2one(comodel_name="res.partner", ondelete="restrict")
    salesperson_id = fields.Many2one(comodel_name="res.users", ondelete="restrict", default=lambda self: self.env.user)
    
    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for area in self:
            area.total_area = area.living_area + area.garden_area
            
    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for property in self:
            property.best_offer = max(property.offer_ids.mapped("price"), default=0)
            
    @api.onchange("garden")
    def _onchange_garden(self):
        self.garden_area = self.garden and 10
        self.garden_orientation = self.garden and "nort"


    def action_sold(self):
        if self.filtered(lambda p: p.state == "canceled"):
            raise UserError(_("A canceled property can not be sold"))
        self.filtered(lambda p: p.state != "sold").write({"state": "sold"})
        return True

    def action_cancel(self):
        if self.filtered(lambda p: p.state == "sold"):
            raise UserError (_("A sold property can not be canceled"))
        self.filtered(lambda p: p.state != "canceled").write({"state": "canceled"})
        return True