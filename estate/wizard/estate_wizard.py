from odoo import fields,models

class estateWizard(models.TransientModel):
    _name = 'estate.buyer.wizard'
    
    partner1_id = fields.Many2one("res.partner", "Instructor", required=True)
    
    def action_buyer(self):
        self.ensure_one()
        activeIds = self.env.context.get('active_ids')
        self.env['estate.property.offer'].browse(activeIds).write({'partner_id': self.partner1_id.id})
        return True

class estateOffer(models.TransientModel):
    _name = 'estate.offer.wizard'
    
    price = fields.Float()
    partner_id = fields.Many2one('res.partner')
    status = fields.Selection([
        ('accepted','Accepted'),
        ('refuse','Refused')
    ])
    
    def action_offer(self):
        self.ensure_one()
        activeIds = self.env.context.get('active_ids')
        data = {
            'price': self.price,
            'partner_id': self.partner_id.id,
            'status': self.status
        }

        for pr in self.env['estate.property'].browse(activeIds):
            pr.write({'offer_ids': [(0, 0, data)]})