from odoo import models, api
from odoo.fields import (
    Char,
    Text,
    Date,
    Float,
    Integer,
    Boolean,
    Selection,
    Date,
    Many2one,
    Many2many,
    One2many,
)


class EstateProperty(models.Model):
    _name = "estate_property"
    _description = "Property of estate"

    # M-1 Relationships ------------------------------------------------------------------
    property_type_id = Many2one("estate_property_type", string="Property Type")
    salesperson_id = Many2one(
        "res.users", string="Salesperson", default=lambda self: self.env.user
    )
    buyer_id = Many2one("res.partner", string="Buyer", copy=False)

    # M-M Relationships ------------------------------------------------------------------
    tag_ids = Many2many("estate_property_tag", string="Tags")

    # 1-M Relationships ------------------------------------------------------------------
    offer_ids = One2many("estate_property_offer", "property_id", string="Offers")

    # Attributes ------------------------------------------------------------------
    name = Char(required=True)
    description = Text()
    postcode = Char()
    date_availability = Date(copy=False, default=Date.add(Date.today(), months=3))
    expected_price = Float(required=True)
    selling_price = Float(readonly=True, copy=False)
    bedrooms = Integer(default=2)
    living_area = Integer()
    facades = Integer()
    garage = Boolean()
    garden = Boolean()
    garden_area = Integer()
    garden_orientation = Selection(
        string="Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
        help="Orientation of garden",
    )

    # Computed fields ------------------------------------------------------------------
    total_area = Float(compute="_compute_total", readonly=True)
    best_price = Float(compute="_compute_best", readonly=True)

    # Reserved fields ------------------------------------------------------------------
    active = Boolean(default=True)
    state = Selection(
        default="new",
        string="State",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        help="State of transaction",
    )

    # Computation Functions ------------------------------------------------------------------
    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best(self):
        for record in self:
            record.best_price = (
                max(record.offer_ids.mapped("price")) if record.offer_ids else 0.0
            )
