from jinja2 import Template


def render_map(appartments, template_name, js_api_key, default_map_center):
    with open(template_name, 'r') as template_file:
        template = Template(template_file.read())
        return template.render(
            appartments=appartments,
            js_api_key=js_api_key,
            map_center=default_map_center,
        )
