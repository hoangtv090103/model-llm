from odoo import models, fields, api


class PromptLog(models.Model):
    _name = "mllm.prompt.log"

    prompt = fields.Text(string="Prompt")
    model = fields.Char(string="Model Name")
    user_id = fields.Many2one(
        "res.users", default=lambda self: self.env.user, string="User"
    )
    state = fields.Selection(
        [
            ("done", "Done"),
            ("cancel", "Cancel"),
        ],
        string="State",
    )
    db_query = fields.Text(string="DB Query")
