# -*- coding: utf-8 -*-

from odoo import fields, models,api
from odoo.tools.float_utils import float_compare
from odoo.exceptions import UserError,ValidationError
import random
#ORM


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table with the property house"
    #_order = "sequence"# a order by, by default when we will ask for the stuff
    _order = "id"

    _check_property_expected_price = models.Constraint(
        'CHECK(expected_price > 0)',
        'A property expected price must be strictly positive',
    )

    _check_property_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'A property selling_price must be strictly positive',
    )


    #string is the first argument, it will show up in the ui, search...
    name = fields.Char(string='Name', required=True, translate=True,default="New House")# translate different for eatch language eng/fr/nl...

    type_id = fields.Many2one("estate.property.type", string="Type of property")
    buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
    saleperson_id = fields.Many2one("res.users",default=lambda self: self.env.user)

    tags_ids = fields.Many2many("estate.property.tags",string="Tags")

    offer_ids = fields.One2many("estate.property.offers",'property_id',string="Offers")#in sql not necessary

    active = fields.Boolean(default=True)
    description = fields.Text(string='Description', translate=True, default="here is somme default description")
    postcode = fields.Char('Postcode',required=True,default=1000)#we do not need integer because we don't do math on that
    date_availability = fields.Date("Available From", default=lambda x:fields.Date.add(fields.Date.today(), months=3), copy=False)#not copy will prevent data to be copied when duplication
    expected_price = fields.Float("Expected Price",required=True,help="hello help expected price !",default=1)
    selling_price =fields.Float("Selling Price",index=True, readonly=True, copy=False,default=0)#odoo will ask postegre to make a index to optimize the search !

    @api.constrains('selling_price')
    def _check_estate_selling_price(self):
        for record in self:


            if record.selling_price == 0:
                break
            if float_compare((record.expected_price * 0.8),record.selling_price,2) > 0:
                raise ValidationError("The selling price must be 80% or more of the expected_price")


    bedrooms = fields.Integer('Number Of Bedrooms',default=2)
    living_area = fields.Integer('Living Area   ')
    facades =fields.Integer('Facade', default=2)
    garage = fields.Boolean('Garage', default=False)#why bool ?? number of garage ?
    garden =fields.Boolean('Garden')
    garden_area =fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Garden Orientation',
        selection=[('north','North'),('south','South'),('east', 'East'),('west','West')])
    state = fields.Selection(string='State', default='new',
        selection=[('new','New'),('offer Received','Offer Received'),('offer Accepted', 'Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')])

    total_space = fields.Float(compute="_compute_balance",string="Total Space")


    @api.depends('garden_area', 'living_area')
    def _compute_balance(self):#self contien tout les bien
        for estate in self:
            estate.total_space = estate.garden_area + estate.living_area#comme self contient plusieur bien en traite un bien à la fois et on enregirste le total pour tout



    max_offer = fields.Float(compute="_compute_max_offer",string="Max offer")

    max_offer_but_with_mapped = fields.Float(compute="_compute_max_offer_mapped",string = "Max offer with mapped ()")


    @api.depends('offer_ids')#use tho instant refresh and refresh with store=True
    def _compute_max_offer(self):

        for estate in self:#we loop on estate
            #print(f"{estate=}")
            estate.max_offer = 0
            for offer in estate.offer_ids:#for eatch estate we loop on every offer
                #print(f"{offer=}")
                if offer.name > estate.max_offer:
                    estate.max_offer = offer.name


    @api.depends('offer_ids')
    def _compute_max_offer_mapped(self):
        print("🎉🎉")
        print(self)

        for estate in self:

            if len(estate.offer_ids) == 0:
                estate.max_offer_but_with_mapped =0
                continue

            #print("🎉🎉")
            #print(estate.offer_ids.mapped('name'))
            estate.max_offer_but_with_mapped =max(estate.offer_ids.mapped('name'))

    @api.onchange('garden')
    def garden_onchange(self):


        for prop in self:

            if prop.garden:

                prop.garden_area = 10

                prop.garden_orientation = 'north'
            else:

                prop.garden_area =None
                prop.garden_orientation = None

    def action_replace_name_by_pomme_de_terre(self):
        print("hello")
        for record in self:
            record.name = "Pomme de terre"
        return True

    def action_replace_name_by_random_coaster_name(self):
        print("hello")
        coaster = ["kondaa","loup-garou","vampire","calamity","mecalodon","turbine","cobra"]
        for record in self:
            key = random.randint(0, len(coaster)-1)
            record.name = coaster[key]
        return True

    def action_set_as_sold(self):

        for record in self:

            if record.state == 'cancelled':
                raise UserError("cannot sold a cancel property")  # exemple d'une erreur
            else:
                record.state = 'sold'

        return True

    def action_set_as_cancel(self):


        for record in self:
            print("🥸")

            if record.state == 'sold':
                print("🥸🥸🥸🥸")
                raise UserError("cannot cancel a sold property")  # exemple d'une erreur
            else:
                record.state = 'cancelled'

        return True







    #New, Offer Received, Offer Accepted, Sold and Cancelled


    #number_of_months = fields.Integer('# Months', required=True)
    #active = fields.Boolean('Active', default=True)
    #sequence = fields.Integer('Sequence', default=10)
