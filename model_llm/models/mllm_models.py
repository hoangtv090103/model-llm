from odoo import models, fields


class MLLMModel(models.Model):
    _name = "mllm.models"

    model = fields.Char(string="Model")
    prompt_log_id = fields.Many2one("mllm.prompt", string="Prompt")

    field_ids = fields.One2many("mllm.fields", "model_id", string="Fields")
