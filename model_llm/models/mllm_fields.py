from odoo import models, fields, api


class MLLMFields(models.Model):
    _name = 'mllm.fields'
    
    model_id = fields.Many2one('mllm.models', string='Model')
    
    name = fields.Char(string='Name')
    type = fields.Char(string='Type')
    relation = fields.Char(string='Relation')
    relation_field = fields.Char(string='Relation Field')
    required = fields.Boolean(string='Required')
    readonly = fields.Boolean(string='Readonly')
    unique = fields.Boolean(string='Unique')
    translate = fields.Boolean(string='Translate')
    store = fields.Boolean(string='Store')
    index = fields.Boolean(string='Index')
    compute = fields.Char(string='Compute')
    inverse = fields.Char(string='Inverse')
    search = fields.Char(string='Search')
    ondelete = fields.Char(string='On Delete')
    domain = fields.Char(string='Domain')
    context = fields.Char(string='Context')
    group = fields.Char(string='Group')
    copy = fields.Char(string='Copy')
    help = fields.Char(string='Help')
    string = fields.Char(string='String')
    selection = fields.Char(string='Selection')
    related = fields.Char(string='Related')
    default = fields.Char(string='Default')
    size = fields.Char(string='Size')
    digits = fields.Char(string='Digits')
    track_visibility = fields.Char(string='Track Visibility')
    attachment = fields.Char(string='Attachment')