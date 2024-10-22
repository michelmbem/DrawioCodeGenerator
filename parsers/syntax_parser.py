import traceback


def parse_class_name(class_name):
    if class_name.startswith("<<"):
        pos = class_name.find(">>")
        if pos >= 0:
            stereotype = class_name[2:pos].strip().lower()
            class_name = class_name[pos + 2:].strip()
        else:
            raise ValueError(f"Invalid type name: {class_name}")
    else:
        stereotype = None

    return class_name, stereotype


def parse_property_signature(property_sig):
    property_sig = property_sig.strip()
    access_modifier_symbol = property_sig[0]
    parts = property_sig[1:].split(":")

    if len(parts) > 1:
        name = parts[0].strip()
        parts = parts[1].split("=")
        data_type = parts[0].strip()
    else:
        data_type = None
        parts = parts[0].split("=")
        name = parts[0].strip()

    default_value = parts[1].strip() if len(parts) > 1 else None

    return access_modifier_symbol, name, data_type, default_value


def parse_method_signature(method_sig):
    method_sig = method_sig.strip()
    access_modifier_symbol = method_sig[0]
    parts = method_sig[1:].split(":")
    name = parts[0].strip()
    return_type = parts[1].strip() if len(parts) > 1 else "void"

    if name.endswith(")"):
        lpar = name.find("(")
        if lpar < 0:
            raise ValueError(f"Malformed method signature: {method_sig}. Missing opening parenthesis")
        else:
            parameters = [s.strip() for s in name[lpar + 1:-1].split(",")]
            name = name[:lpar].strip()
    else:
        parameters = []

    return access_modifier_symbol, name, parameters, return_type


class SyntaxParser:
    """
    Parse the style tree into the syntax tree

    Parameters:
      style_tree: style tree of the drawio file
    """

    def __init__(self, style_tree):
        self.style_tree = style_tree

    def convert_to_syntax_tree(self):
        """
        Convert the style tree to syntax tree

        Returns:
          syntax_tree: the syntax tree that is used by the generators
        """

        print("<<< CONVERTING STYLE TREE TO SYNTAX TREE >>>")

        syntax_tree = {}

        try:
            cells = self.style_tree['root']['cells']
            relationships = self.style_tree['root']['relationships']
            parent = self.style_tree['root']['id']

            properties_done = False
            _id = 0

            for key, value in cells.items():
                if value['parent_id'] in relationships.keys() or "endArrow" in value['style'].keys():
                    # skip the label for relationships
                    continue

                if value['parent_id'] == parent and value['style']['type'].lower() in ('swimlane', 'html', 'text'):
                    # start of a new cell
                    syntax_tree[key] = self._tree_template(value)
                    properties_done = False
                    _id = 0
                else:
                    # properties and methods in the cell
                    if value['style']['type'].lower() == 'line' and value['parent_id'] in syntax_tree.keys():
                        # line separating the properties and methods
                        properties_done = True
                        _id = 0
                    else:
                        if properties_done:  # methods
                            syntax_tree[value['parent_id']]['methods'] = {
                                **syntax_tree[value['parent_id']]['methods'],
                                **self._methods_template(value, _id)
                            }
                        else:  # properties
                            syntax_tree[value['parent_id']]['properties'] = {
                                **syntax_tree[value['parent_id']]['properties'],
                                **self._properties_template(value, _id)
                            }

                        _id += len(value['values'])

            for relationship in relationships.keys():
                self._add_relationships(syntax_tree, relationships[relationship])
        except Exception as e:
            print(f"SyntaxParser.convert_to_syntax_tree ERROR: {e}")
            traceback.print_exception(e)

        return syntax_tree

    def _tree_template(self, main_cell):
        """
        Create the template that will house each cell

        Parameters:
          main_cell: the starting, parent cell

        Returns:
          template: the starting template (dictionary)
        """

        template = {
            'type': "class",
            'name': main_cell['values'][0] if len(main_cell['values']) > 0 else "",
            'stereotype': None,
            'properties': {},
            'methods': {},
            'relationships': {
                'implements': [],
                'extends': [],
                'association': [],
                'aggregation': [],
                'composition': []
            }
        }

        if main_cell['style']['type'] in ("html", "text"):
            values_length = len(main_cell['values'])
            name = main_cell['values'][0] if values_length > 0 else ""
            properties = {'values': main_cell['values'][1] if values_length > 1 else None}
            methods = {'values': main_cell['values'][2] if values_length > 2 else None}

            template['name'] = name[0]
            template['properties'] = self._properties_template(properties, 0) or {}
            template['methods'] = self._methods_template(methods, 0) or {}

        name, stereotype = parse_class_name(template['name'])
        template['name'] = name

        if stereotype == "abstract":
            template['type'] = "abstract class"
        elif stereotype in ("interface", "enum"):
            template['type'] = stereotype
        else:
            template['stereotype'] = stereotype

        return template

    def _properties_template(self, property_dict, _id):
        """
        Create the template for properties

        Parameters:
          property_dict: the properties dictionary from the style tree
          _id: id for the keys in the dictionary

        Returns:
          template: the properties template (dictionary)
        """

        values = property_dict['values']
        template = {}

        if values:
            for val in values:
                if len(val) == 0:
                    continue

                _id += 1
                access_modifier_symbol, name, data_type, default_value = parse_property_signature(val)
                template[_id] = {
                    'access': self._get_access_modifier(access_modifier_symbol),
                    'name': name,
                    'type': data_type,
                    'default_value': default_value,
                }

        return template

    def _methods_template(self, method_dict, _id):
        """
        Create the template for methods

        Parameters:
          method_dict: the methods dictionary from the style tree
          _id: id for the keys in the dictionary

        Returns:
          template: the methods template (dictionary)
        """

        values = method_dict['values']
        template = {}

        if values:
            for val in values:
                if len(val) == 0:
                    continue

                _id += 1
                access_modifier_symbol, name, parameters, return_type = parse_method_signature(val)
                template[_id] = {
                    'access': self._get_access_modifier(access_modifier_symbol),
                    'name': name,
                    'parameters': parameters,
                    'return_type': return_type,
                }

        return template

    def _get_access_modifier(self, symbol):
        """
        Return the access modifier

        Parameters:
          symbol: symbol representing the access modifier

        Returns:
          text: the text of the access modifier symbol
        """

        access_modifier_dict = {
            '+': "public",
            '#': "protected",
            '-': "private"
        }

        return access_modifier_dict[symbol]

    def _add_relationships(self, syntax_tree, relationship):
        """
        Add the relationship for the cells in the syntax tree

        Parameters:
          syntax_tree: the syntax_tree dictionary
          relationship: relationship to be added to the syntax tree
        """

        source = relationship['source']
        target = relationship['target']
        style = relationship['style']

        source_cell = syntax_tree[source]
        target_cell = syntax_tree[target]

        if "endArrow" in style.keys() and style['endArrow'].lower() in ("block", "none"):
            if style['endArrow'].lower() == "none" or style['endFill'].lower() == "1":
                # association
                target_cell['relationships']['association'] += [source]
            elif "dashed" in style.keys() and style['dashed'] == "1":
                # implements
                source_cell['relationships']['implements'] += [target]
            else:
                # extends
                source_cell['relationships']['extends'] += [target]
        elif ("endArrow" in style.keys() and style['endArrow'].lower() == "diamondthin") or \
                ("startArrow" in style.keys() and style['startArrow'].lower() == "diamondthin"):
            if "endFill" in style.keys() and style['endFill'] == "1":
                # composition
                target_cell['relationships']['composition'] += [source]
            else:
                # aggregation
                target_cell['relationships']['aggregation'] += [source]
