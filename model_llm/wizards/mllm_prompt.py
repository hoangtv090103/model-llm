from odoo import models, fields, tools
import google.generativeai as genai
import os
from odoo.tools.config import config

from odoo.models import BaseModel


API_KEY = config.get("genai_api")

genai.configure(api_key=API_KEY)

model = genai.GenerativeModel(
    "gemini-1.5-flash", generation_config={"response_mime_type": "application/json"}
)


class Prompt(models.TransientModel):
    _name = "mllm.prompt"
    _description = "Prompt"

    model = fields.Char(string="Model Name")
    prompt = fields.Text(string="Prompt")

    def action_prompt(self):
        try:
            log_id = self.env["mllm.prompt.log"].create({"prompt": self.prompt})

            prompt = f"Please give me fields and fields' attributes of models (words separate by '.') in Odoo with format like JSON. \nDetail: {self.prompt}"
            response = model.generate_content(prompt)
            # model_name = self.model.replace(".", "_")

            # JSON to dict
            response_text = response.text.replace("true", "True").replace(
                "false", "False"
            )
            models_data = eval(response_text)

            for model_name, fields in models_data.items():
                # Check if model exists
                model_obj = self.env["ir.model"].search([("model", "=", model_name)])
                if model_obj:
                    log_id.db_query = (
                        log_id.db_query or ""
                    ) + f"\n[Fail] Model {model_name} already exists"
                    continue

                # TODO: Fix cannot create model
                model_obj = self.env["ir.model"].create(
                    {
                        "name": self.model,
                        "model": model_name,
                        "state": "manual",
                    }
                )
                field_objs = self.env["ir.model.fields"]

                for field in fields:
                    ttype = field.pop("type")
                    field_objs += field_objs.create(
                        field.update({"model_id": model_obj.id, "ttype": ttype}),
                    )

            return
        except Exception as e:
            self.env["mllm.prompt.log"].create(
                {
                    "prompt": self.prompt,
                    "model": self.model,
                    "state": "cancel",
                    "db_query": f"[Fail] {str(e)}",
                }
            )
            return

    def create_view(self, model_name):
        self._cr.execute(
            """
            CREATE OR REPLACE VIEW %s AS
            SELECT * FROM %s
        """
            % (model_name.replace(".", "_"), model_name)
        )
        self._cr.commit()
