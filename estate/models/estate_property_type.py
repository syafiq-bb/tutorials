from odoo import models
from odoo.fields import Char


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Types of Estate Property"

    name = Char(required=True)
