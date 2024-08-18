import os
import re
import shutil

from bs4 import BeautifulSoup, NavigableString
from jinja2 import Template, Undefined, Environment
from typing import Any, Dict, List
import copy


class HtmlTemplate:
    def __init__(self):
        self.name: str = ''  # Name of the file
        self.path: str = ''  # Path to the file
        self.content: str = ''  # Content of the file


debbugFolder = 'C:\\Users\\ja\\PycharmProjectsss\\Tement\\output'
templatesPath: str = 'C:\\Users\\ja\\PycharmProjectsss\\Tement\\elements'
templates: Dict[str, HtmlTemplate] = {}
# Configure the environment to allow undefined variables
env = Environment(undefined=Undefined)
counter = 0


def init():
    if not os.path.exists(templatesPath):
        raise Exception(f"The directory {templatesPath} does not exist.")

    for root, dirs, files in os.walk(templatesPath):
        for file in files:
            file_name = os.path.splitext(file)[0]

            if file_name in templates:
                raise Exception(f"Duplicate file name found: {file_name}")

            template = HtmlTemplate()
            template.name = file_name.lower()
            template.path = os.path.join(root, file)

            with open(template.path, 'r', encoding='utf-8') as f:
                template.content = f.read()

            templates[template.name] = template

    print(f"Successfully loaded {len(templates)} templates.")
    if os.path.exists(debbugFolder):
        shutil.rmtree(debbugFolder)
    os.makedirs(debbugFolder)


body_children = {}


def parse(template_name: str, context: Any) -> str:
    template = find_template(template_name)
    parsed = parse_template(template.name, template.content, context)

    body_element = parsed.find('body')
    if body_element is None:
        return parsed.prettify()

    values_ids = []
    for children in body_children.values():
        for name, values in children.items():
            for value in values:
                if 'id' in value.attrs:
                    values_ids.append((parse_int(value['id'], 0), value))
                else:
                    values_ids.append((0, value))
    # Sort the list of tuples by the first element in the tuple, which is the id
    sorted_values_ids = sorted(values_ids, key=lambda x: x[0])

    for value in sorted_values_ids:
        body_element.append(value[1])

    return parsed.prettify()


render_index = 0


def parse_template(template_name: str, template_content: str, context: Any) -> BeautifulSoup:
    jinja_template = env.from_string(template_content)
    rendered_html = jinja_template.render(context)

    soup = BeautifulSoup(rendered_html, 'html.parser')

    body_content = {
        'scripts': soup.find_all('script'),
        'styles': soup.find_all('style')
    }

    body_children[template_name] = body_content

    for elements in body_content.values():
        for element in elements:
            element.extract()

    for template in templates.values():
        name = template.name.lower()
        elements = soup.find_all(name)
        for element in elements:
            print(template.name)
            fragment_element = handle_fragment_element(template, element, context)
            element.replace_with(fragment_element.find())

    return soup


def handle_fragment_element(template: HtmlTemplate, element: Any, context: Any) -> BeautifulSoup:
    print(template.name)
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
    soup = parse_template(template.name, content, context)
    top_element = soup.find()
    for attr_name, attr_value in attributes.items():
        top_element[attr_name] = attr_value

    # Looking for the content nodes
    sections = {}
    sections['content'] = []
    for child in element.children:
        if isinstance(child, NavigableString):
            continue

        child_name = child.name.split('.')
        if len(child_name) < 2:
            sections['content'].append(copy.deepcopy(child))
            continue
        if child_name[0] != template.name:
            sections['content'].append(copy.deepcopy(child))
            continue

        section_name = child_name[1]
        sections[section_name] = copy.deepcopy(child.children)

    # Placing html in the content nodes
    for name, value in sections.items():
        section_name = f'content.{name}'
        if name == 'content':
            section_name = 'content'

        section_element = soup.find(section_name)
        if section_element is None:
            continue

        section_element.name = 'div.' + template.name + '.' + name

        #
        # for attr_name, attr_value in value.attrs.items():
        #     section_element[attr_name] = attr_value

        for child in value:
            section_element.append(child)

    global render_index
    render_index += 1
    with open(debbugFolder + "/" + str(render_index) + "." + template.name + '.html', 'w') as f:
        f.write(soup.prettify())

    return soup


def find_template(template_name: str) -> HtmlTemplate:
    template_name = template_name.lower()
    if '.html' in template_name:
        template_name = template_name.replace('.html', '')

    if template_name not in templates:
        raise Exception(f"Template {template_name} not found.")
    template = templates[template_name]
    return template


def parse_int(value, default=0):
    try:
        return int(value)
    except (ValueError, TypeError):
        return default
