# -*- coding: utf-8 -*-

from odoo import fields, models, api
#ORM


class EstateProperty(models.Model):
    _name = "estate.property.offers"
    _description = "Table with the offers for the property"
    #_order = "sequence"# a order by, by default when we will ask for the stuff
    _order = "name desc"


    _check_property_offer_price = models.Constraint(
        'CHECK(name > 0)',
        'An offer price must be strictly positive',
    )
    #yeah meaby i need to change that name = Float
    name = fields.Float("Expected Price",required=True,default=1)

    status = fields.Selection(string='Status', copy=False,
        selection=[('accepted','Accepted'),('refused','Refused')])

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)


    validity =fields.Integer("Day left",default=7)

    date_deadline = fields.Date("Date limite offre",compute='_compute_offer_deadline',inverse='_inverse_days')

    @api.depends('validity')  # use tho instant refresh and refresh with store=True
    def _compute_offer_deadline(self):
        for offers in self:
            temp = fields.Date.today()
            if offers.create_date:
                temp = offers.create_date.date()


            offers.date_deadline = fields.Date.add(temp, days=offers.validity)


    @api.onchange('date_deadline')#use to refresh the interface only
    def _inverse_days(self):
        for offers in self:
            temp =fields.Date.today()
            if offers.create_date:
                temp = offers.create_date.date()
            offers.validity = (offers.date_deadline- temp).days



    def action_confirm_offer(self):
        for offer in self:
            offer.status = 'accepted'

            offer.property_id.selling_price = offer.name
            offer.property_id.buyer_id = offer.partner_id

            offer.property_id.state = "offer Accepted"

    def action_refuse_offer(self):
        for offer in self:
            offer.status = 'refused'





    #string is the first argument, it will show up in the ui, search...
    #name = fields.Char(string='Name', required=True, translate=True)# translate different for eatch language eng/fr/nl...
    #active = fields.Boolean(default=True)
    #description = fields.Text(string='Description', translate=True, default="here is somme default description")
    #postcode = fields.Char('Postcode',required=True)#we do not need integer because we don't do math on that
    #date_availability = fields.Date("Available From", default=lambda x:fields.Date.add(fields.Date.today(), months=3), copy=False)#not copy will prevent data to be copied when duplication
    #expected_price = fields.Float("Expected Price",required=True,help="hello help expected price !")
    #selling_price =fields.Float("Selling Price",index=True, readonly=True, copy=False)#odoo will ask postegre to make a index to optimize the search !
    #bedrooms = fields.Integer('Number Of Bedrooms',default=2)
    #living_area = fields.Integer('Living')
    #facades =fields.Integer('Facade', default=2)
    #garage = fields.Boolean('Garage', default=False)#why bool ?? number of garage ?
    #garden =fields.Boolean('Garden')
    #garden_area =fields.Integer('Garden Area')
    #garden_orientation = fields.Selection(string='Garden Orientation',
    #    selection=[('north','North'),('south','South'),('east', 'East'),('west','West')])
    #state = fields.Selection(string='State', default='new',
    #    selection=[('new','New'),('offer Received','Offer Received'),('offer Accepted', 'Offer Accepted'),('sold','Sold'),('cancelled','Cancelled')])
#
    #New, Offer Received, Offer Accepted, Sold and Cancelled


    #number_of_months = fields.Integer('# Months', required=True)
    #active = fields.Boolean('Active', default=True)
    #sequence = fields.Integer('Sequence', default=10)
