import traceback


def parse_class_name(class_name):
    class_modifier = None
    delimiters = [("<<", ">>"), ("&lt;&lt;", "&gt;&gt;")]

    for delimiter in delimiters:
        if class_name.startswith(delimiter[0]):
            pos = class_name.find(delimiter[1])
            if pos >= 0:
                class_modifier = class_name[len(delimiter[0]):pos].strip()
                class_name = class_name[pos + len(delimiter[1]):].strip()
            else:
                raise ValueError(f"Invalid type name: {class_name}")
            break

    return class_name, class_modifier


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

                _style_type = value['style']['type'].lower()

                if value['parent_id'] == parent and _style_type in ('swimlane', 'html', 'text'):
                    # start of a new cell
                    syntax_tree[key] = self._tree_template(value)
                    properties_done = False
                    _id = 0
                else:
                    # properties and methods in the cell
                    if _style_type == 'line' and value['parent_id'] in syntax_tree.keys():
                        # line separating the properties and methods
                        properties_done = True
                        _id = 0
                    else:
                        if not properties_done:  # properties
                            syntax_tree[value['parent_id']]['properties'] = {
                                **syntax_tree[value['parent_id']]['properties'],
                                **self._properties_template(value, _id)}
                            _id += len(value['values'])
                        else:  # methods
                            syntax_tree[value['parent_id']]['methods'] = {**syntax_tree[value['parent_id']]['methods'],
                                                                          **self._methods_template(value, _id)}
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

        class_name, class_modifier = parse_class_name(template['name'])
        template['name'] = class_name

        if class_modifier == "abstract":
            template['type'] = "abstract class"
        elif class_modifier == "interface":
            template['type'] = "interface"
        elif class_modifier == "enum":
            template['type'] = "enum"

        return template

    def _properties_template(self, property_dict, _id):
        """
        Create the template for properties

        Parameters:
          property_dict: the properties dictionary from the style tree
          _id: id for the keys in the dictionary

        Returns:
          template: the properties tempate (dictionary)
        """

        values = property_dict['values']
        template = {}

        if values:
            for val in values:
                if len(val) == 0:
                    continue

                _id += 1

                val = val.strip()
                access_modifier_symbol = val[0]
                temp_val = val[1:].split(":")

                template[_id] = {
                    'access': self._get_access_modifier(access_modifier_symbol),
                    'name': temp_val[0].strip(),
                    'type': temp_val[1].strip() if len(temp_val) > 1 else None,
                }

        return template

    def _methods_template(self, method_dict, _id):
        """
        Create the template for methods

        Parameters:
          method_dict: the methods dictionary from the style tree
          _id: id for the keys in the dictionary

        Returns:
          template: the methods tempate (dictionary)
        """

        values = method_dict['values']
        template = {}

        if values:
            for val in values:
                if len(val) == 0:
                    continue

                _id += 1

                val = val.strip()
                access_modifier_symbol = val[0]
                temp_val = val[1:].split(":")

                template[_id] = {
                    'access': self._get_access_modifier(access_modifier_symbol),
                    'name': temp_val[0].strip(),
                    'return_type': temp_val[1].strip() if len(temp_val) > 1 else "void",
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
