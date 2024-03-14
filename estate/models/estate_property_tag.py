from odoo import models
from odoo.fields import Char


class EstatePropertyTag(models.Model):
    _name = "estate_property_tag"
    _description = "Tags for Estate Property"

    name = Char(required=True)
