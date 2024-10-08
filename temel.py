import os
import re
import shutil

from bs4 import BeautifulSoup, NavigableString
from jinja2 import Undefined, Environment
from typing import Any, Dict, List
import copy


class HtmlTemplate:
    def __init__(self):
        self.name: str = ''  # Name of the file
        self.path: str = ''  # Path to the file
        self.content: str = ''  # Content of the file


_templates: Dict[str, HtmlTemplate] = {}
_SLOT_NAME = 'slot'
_jinja_env = Environment(undefined=Undefined)
_body_children = {}
_render_index = 0

_debug = False
_debug_path = ''


def enable_debug(is_debug: bool = True, debug_output: str = ''):
    global _debug
    _debug = is_debug

    global _debug_path
    _debug_path = debug_output


def load_templates(templatesPath: str):
    if _debug:
        print(f"Debug mode enabled!")

    if not os.path.exists(templatesPath):
        raise Exception(f"The directory {templatesPath} does not exist.")

    for root, dirs, files in os.walk(templatesPath):
        for file in files:
            file_name = os.path.splitext(file)[0]

            if file_name in _templates:
                raise Exception(f"Duplicate file name found: {file_name}")

            template = HtmlTemplate()
            template.name = file_name.lower()
            template.path = os.path.join(root, file)

            with open(template.path, 'r', encoding='utf-8') as f:
                template.content = f.read()

            _templates[template.name] = template

    if _debug:
        print(f"Successfully loaded {len(_templates)} templates.")
        if os.path.exists(_debug_path):
            shutil.rmtree(_debug_path)
        os.makedirs(_debug_path)


def parse(template_name: str, context: Any) -> str:
    global _render_index
    _render_index = 0

    template = _find_template(template_name)
    parsed = _parse_template(template.name, template.content, context)

    body_element = parsed.find('body')
    if body_element is None:
        body_element = parsed.find()

    values_ids = []
    for children in _body_children.values():
        for name, values in children.items():
            for value in values:
                if 'id' in value.attrs:
                    values_ids.append((_parse_int(value['id'], 0), value))
                else:
                    values_ids.append((0, value))
    # Sort the list of tuples by the first element in the tuple, which is the id
    sorted_values_ids = sorted(values_ids, key=lambda x: x[0])

    for value in sorted_values_ids:
        body_element.append(value[1])

    return parsed.prettify()


def _parse_template(template_name: str, template_content: str, context: Any) -> BeautifulSoup:
    jinja_template = _jinja_env.from_string(template_content)
    rendered_html = jinja_template.render(context)

    soup = BeautifulSoup(rendered_html, 'html.parser')

    body_content = {
        'scripts': soup.find_all('script'),
        'styles': soup.find_all('style')
    }

    _body_children[template_name] = body_content

    for elements in body_content.values():
        for element in elements:
            element.extract()

    for template in _templates.values():
        name = template.name.lower()
        elements = soup.find_all(name)
        for element in elements:
            fragment_element = _handle_fragment_element(template, element, context)
            if fragment_element.find() is None:
                continue
            element.replace_with(fragment_element.find())

    return soup


def _handle_fragment_element(template: HtmlTemplate, element: Any, context: Any) -> BeautifulSoup:
    content = template.content
    attributes = {}
    # Getting all attributes for the element, and saving it to array
    for attr_name, attr_value in element.attrs.items():

        if isinstance(attr_value, List):
            attr_value = attr_value[0]

        pattern = r"\{\{\s*" + re.escape(attr_name) + r"\s*\}\}"
        content = re.sub(pattern, attr_value, content)
        attributes[attr_name] = attr_value

    # Passing Arguments to the most top element of Rendered fragment
    soup = _parse_template(template.name, content, context)
    top_element = soup.find()
    for attr_name, attr_value in attributes.items():
        top_element[attr_name] = attr_value

    # Looking for the slots nodes
    slots = {}
    slots_parents = {}
    slots[_SLOT_NAME] = []

    for child in element.children:
        if isinstance(child, NavigableString):
            slots[_SLOT_NAME].append(copy.deepcopy(child))
            continue

        child_name = child.name.split('.')
        if len(child_name) < 2:
            slots[_SLOT_NAME].append(copy.deepcopy(child))
            continue
        if child_name[0] != template.name:
            slots[_SLOT_NAME].append(copy.deepcopy(child))
            continue

        section_name = child_name[1]
        slots[section_name] = copy.deepcopy(child.children)
        slots_parents[section_name] = child

    # Placing html in the slots nodes
    for name, slot_children in slots.items():
        section_name = f'{_SLOT_NAME}.{name}'
        if name == _SLOT_NAME:
            section_name = _SLOT_NAME

        section_element = soup.find(section_name)
        if section_element is None:
            continue

        if _debug:
            section_element.name = 'div.' + template.name + '.' + name
        else:
            section_element.name = 'div'

        for child in slot_children:
            section_element.append(child)

        if name in slots_parents:
            parent_element = slots_parents[name]
            for attr_name, attr_value in parent_element.attrs.items():
                section_element[attr_name] = attr_value

    if _debug:
        global _render_index
        _render_index += 1
        with open(_debug_path + "/" + str(_render_index) + "." + template.name + '.html', 'w') as f:
            f.write(soup.prettify())

    return soup


def _find_template(template_name: str) -> HtmlTemplate:
    template_name = template_name.lower()
    if '.html' in template_name:
        template_name = template_name.replace('.html', '')

    if template_name not in _templates:
        raise Exception(f"Template {template_name} not found.")
    template = _templates[template_name]
    return template


def _parse_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
