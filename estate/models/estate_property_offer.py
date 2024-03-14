from odoo import models
from odoo.fields import Float, Selection, Many2one


class EstatePropertyOffer(models.Model):
    _name = "estate_property_offer"
    _description = "Offers for Estate Property"

    # M-1 Relationships
    partner_id = Many2one("res.partner", string="Partner", required=True)
    property_id = Many2one("estate_property", string="Property", required=True)

    # Attributes
    price = Float()
    status = Selection(
        copy=False, selection=[("accepted", "Accepted"), ("refused", "Refused")]
    )
