import os
from jinja2 import Environment, FileSystemLoader, TemplateNotFound

templates_dir = "templates"
if not os.path.exists(templates_dir):
    os.makedirs(templates_dir, exist_ok=True)

env = Environment(loader=FileSystemLoader(templates_dir))

def render_template(name: str, context: dict) -> str:
    try:
        tpl = env.get_template(f"{name}.txt")
        return tpl.render(**context)
    except TemplateNotFound:
        try:
            default_msg = context.get("message", context.get("body", ""))
            if default_msg:
                return default_msg
            return f"Template {name}.txt not found. Using default message."
        except Exception:
            return f"Template {name}.txt not found."
    except Exception as e:
        return f"Template error: {str(e)}"
