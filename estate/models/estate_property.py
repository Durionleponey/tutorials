# -*- coding: utf-8 -*-

from odoo import fields, models,api
#ORM


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table with the property house"
    #_order = "sequence"# a order by, by default when we will ask for the stuff

    #string is the first argument, it will show up in the ui, search...
    name = fields.Char(string='Name', required=True, translate=True)# translate different for eatch language eng/fr/nl...

    type_id = fields.Many2one("estate.property.type", string="Type of property")
    buyer_id = fields.Many2one("res.partner",string="Buyer",copy=False)
    saleperson_id = fields.Many2one("res.users",default=lambda self: self.env.user)

    tags_ids = fields.Many2many("estate.property.tags",string="Tags")

    offer_ids = fields.One2many("estate.property.offers",'property_id',string="Offers")#in sql not necessary

    active = fields.Boolean(default=True)
    description = fields.Text(string='Description', translate=True, default="here is somme default description")
    postcode = fields.Char('Postcode',required=True)#we do not need integer because we don't do math on that
    date_availability = fields.Date("Available From", default=lambda x:fields.Date.add(fields.Date.today(), months=3), copy=False)#not copy will prevent data to be copied when duplication
    expected_price = fields.Float("Expected Price",required=True,help="hello help expected price !")
    selling_price =fields.Float("Selling Price",index=True, readonly=True, copy=False)#odoo will ask postegre to make a index to optimize the search !
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

    max_offer_but_with_mapped = fields.Float(compute="_compute_max_offer_mapped",string = "Max offer with mapped")


    @api.depends('offer_ids')
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

        for estate in self:
            #print("🎉🎉")
            #print(estate.offer_ids.mapped('name'))
            estate.max_offer_but_with_mapped =max(estate.offer_ids.mapped('name'))



    #New, Offer Received, Offer Accepted, Sold and Cancelled


    #number_of_months = fields.Integer('# Months', required=True)
    #active = fields.Boolean('Active', default=True)
    #sequence = fields.Integer('Sequence', default=10)
