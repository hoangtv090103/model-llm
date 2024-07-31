from odoo import models, fields, tools
import google.generativeai as genai
import os

from odoo.models import BaseModel



genai.configure(api_key="AIzaSyD3tsoyQfSvqodSRW-bONxMLCJoM6u77Kw")

model = genai.GenerativeModel("gemini-1.5-flash")

DATATYPES = {
    'int': int,
    'bigint': int,
    'bigserial': int,
    'bit': int,
    'boolean': bool,
    'char': str,
    'varchar': str,
    'text': str,
    'citext': str,
    'date': 'datetime.date',
    'datetime': 'datetime.datetime',
    'decimal': float,
    'double precision': float,
    'float4': float,
    'float8': float,
    'integer': int,
    'interval': 'datetime.timedelta',
    'json': dict,
    'jsonb': dict,
    'numeric': float,
    'real': float,
    'serial': int,
    'smallint': int,
    'smallserial': int,
    'time': 'datetime.time',
    'timestamp': 'datetime.datetime',
    'timestamptz': 'datetime.datetime',
    'uuid': 'uuid.UUID',
    'xml': str,
}

class Prompt(models.TransientModel):
    _name = "mllm.prompt"
    _description = "Prompt"

    model = fields.Char(string="Model Name")
    prompt = fields.Text(string="Prompt")

    def action_prompt(self):
        try:
            prompt = f"Write Postgresql query to create a model with name: {self.model}. \nDetail: {self.prompt}"
            response = model.generate_content(prompt)

            # Only get the SQL query
            response_text = response.text
            sql_query = response_text.split("```sql")[1].split("```")[0].strip()

            # Get model name
            sql_model_name = sql_query.split("CREATE TABLE ")[1].split(" ")[0]
            model_name = sql_model_name.replace("_", ".") 

            new_model = self.env["ir.model"].create(
                {
                    "name": model_name,
                    "model": model_name,
                    "state": "manual",
                    "access_ids": [(6, 0, [self.env.ref("base.group_user").id])],
                }
            )
            
            # Check if model exists
            model_obj = self.env["ir.model"].search([("model", "=", model_name)])
            if model_obj:
                self.env["mllm.prompt.log"].create(
                    {
                        "prompt": self.prompt,
                        "model": self.model,
                        "state": "cancel",
                        "db_query": f"[Fail] Model {model_name} already exists.",
                    }
                )
                return

            field_definitions = {}
            for line in sql_query.split("\n")[1:]:
                if line and line not in ["(", ");"]:
                    line = line.strip().replace('"', "")
                    field_name = line.split(" ")[0]
                    field_type = line.split(" ")[1]
                    field_type = DATATYPES.get(field_type.lower(), str)
                    field_definitions[field_name] = (field_type, None)


            # Save the prompt log
            self.env["mllm.prompt.log"].create(
                {
                    "prompt": self.prompt,
                    "model": self.model,
                    "db_query": sql_query,
                    "state": "done",
                }
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
