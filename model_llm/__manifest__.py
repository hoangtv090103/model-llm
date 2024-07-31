{
    "name": "Model LLM",
    "summary": "Model LLM",
    "version": "1.0",
    "category": "Model",
    "author": "hoangtv",
    "depends": ["base", "web"],
    "data": [
        # Wizards
        "wizards/mllm_prompt.xml",
        # Views
        "views/mllm_prompt_log.xml",
        "views/mllm_fields.xml",
        "views/mllm_models.xml",
        # Security
        "security/ir.model.access.csv",
        # Menu
        "views/menus.xml",
    ]
       
}