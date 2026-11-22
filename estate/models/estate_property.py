# -*- coding: utf-8 -*-

from odoo import fields, models
#ORM


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Table with the property house"
    _order = "sequence"# a order by, by default when we will ask for the stuff

    #string is the first argument, it will show up in the ui, search...
    name = fields.Char(string='Name', required=True, translate=True)# translate different for eatch language eng/fr/nl...
    description = fields.Text(string='Description', translate=True)
    postcode = fields.Char('Postcode',required=True)#we do not need integer because we don't do math on that
    date_availability = fields.Date("Available From")#buit in
    expected_price = fields.Float("Expected Price")
    selling_price =fields.Float("Selling Price")
    bedroom = fields.Integer('Number Of Bedrooms')
    living = fields.Integer('Living')
    facade =fields.Integer('Facade', default=2)
    garage = fields.Boolean('Garage', default=False)#why bool ?? number of garage ?
    garden =fields.Boolean('Garden')
    garden_area =fields.Integer('Facade')
    garden_orientation = fields.Char('Garden orientation')

    print(f'{garden=}')


    #number_of_months = fields.Integer('# Months', required=True)
    #active = fields.Boolean('Active', default=True)
    #sequence = fields.Integer('Sequence', default=10)
