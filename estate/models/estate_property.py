from odoo import models,fields,api,_
from datetime import date, datetime, timedelta
from odoo.exceptions import UserError, ValidationError

#class Buyer_partner(models.Model):
#
#    _inherit = 'res.partner'
#
#    is_buyer = fields.Boolean(domain="[('is_buyer', '=', ['True'])]")

class EstatePropertyTag(models.Model):
    _name="estate.property.tag"
    _description="Estate property tag"

    name = fields.Char()

# class EstateProduct(models.Model):
#     _name="estate.product"
#     _description="Estate Product"

#     p_name = fields.Char()
#     P_type = fields.Char()

class EstatePropertyType(models.Model):
    _name="estate.property.type"
    _description="Estate property type"

    name = fields.Char()

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate_Property"

    def _get_description(self):
        if self.env.context.get('is_my_property'):
            return self.env.user.name 
    

    name = fields.Char(default = "Unkhown")
    description = fields.Text(default = _get_description)
    postcode = fields.Char()
    property_name = fields.Char()

    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy= False)
    expected_price = fields.Float()
    selling_price = fields.Float(copy= False)
    bedrooms = fields.Integer(default= 2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
    	("North", "North"),
    	("South", "South"),
    	("East", "East"),
    	("West", "West")
    	])
    active = fields.Boolean(default=True)
    image = fields.Image()
    property_type_id = fields.Many2one("estate.property.type")

    property_tag_id = fields.Many2many("estate.property.tag")

    offer_ids = fields.One2many("estate.property.offer", "property_id")

    buyer_id = fields.Many2one('res.partner')
    #buyer_id=fields.Char(required= True,default= "Krishant")

    salse_person=fields.Many2one('res.users', string='SalesPerson', index=True, tracking=True, default=lambda self: self.env.user)
    #sales_person=fields.Char(default="Agent",readonly=True)

    total_area= fields.Float(compute = '_compute_total_area',inverse= '_inverse_total_area')

    pname=fields.Char(related='property_type_id.name',string = "Property Name")
    status = fields.Selection([("new", "New"),("Offer Received", "Offer Received"),("Offer Accepted", "Offer Accepted"),("sold","Sold"),("cancel", "Cancel")],default="new")
    
    def action_do_sold(self):
        for record in self:
            if record.status == 'cancel' :
                raise UserError("Don't sold order")
            record.status = "sold"
        
    def action_do_cancel(self):
        for record in self:
            if record.status == 'sold' :
                raise UserError("Don't cancled order")
            record.status = "cancel"


    #best_price = fields.Float()

  
    
   
    
    @api.depends('living_area','garden_area')
    def _compute_total_area(self):
   #class compute_total_area():
       for record in self:
            record.total_area = record.living_area + record.garden_area
    def _inverse_total_area(self):
        for record in self:
            record.total_area = (record.living_area + record.garden_area) / 2

    @api.constrains('living_area','garden_area')
    def _check_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden area cannot be bigger than living area")

    @api.constrains('expected_price')
    def _check_area(self):
        for record in self:
            if record.expected_price < 1:
                raise UserError("Price should be positive")


    @api.onchange('garden')
    def _garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 100
                record.garden_orientation = 'North'
            else:
                record.garden_area = 0
                record.garden_orientation = None


    def open_offers(self):
        view_id_all = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_all, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
            }

    def open_confirm_offers(self):
        view_id_accept = self.env.ref('estate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id_accept, 'tree']],
            # "res_id": 2,
            # "target":"new",
            "domain": [('property_id', '=', self.id),('status','=','accepted')]
            }

    
class Buyer(models.Model):
    _name = "buyers"
    _description = "Buyer"

    buyer = fields.Char()

class Sales_Person(models.Model):
    _name = "sales.person"
    _description = "Sales Person"

    sales_person = fields.Char()

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"


    price = fields.Float()
    status = fields.Selection([('accepted','accepted'),('refused','refused')])
    partner_id = fields.Many2one("res.partner",required = True)
    property_id = fields.Many2one("estate.property", required = True)
    
    validity = fields.Integer()
    date_deadline = fields.Date(compute = '_compute_date_deadline',inverse = '_inverse_date')
    
    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity and record.create_date:
                record.date_deadline = record.create_date + timedelta(days = record.validity)
            else:
                record.date_deadline = False

    @api.depends('date_deadline')
    def _inverse_date(self):
        for record in self:
           if record.date_deadline:
                   record.validity = int((record.date_deadline - (record.create_date).date()).days)



    #def action_do_cancel(self):
    #    for record in self:
    #        record.name = "Cencel"
    #    return True

    def action_do_accepted(self):
        for record in self:
            if record.status == "refused":
                raise UserError("Refused offer cannot be accepted")
            record.status = "accepted"
                


    def action_do_refused(self):
        for record in self:
            if record.status=="accepted":
                raise UserError("Accepted offer cannot be Refused")
            record.status = "refused"

