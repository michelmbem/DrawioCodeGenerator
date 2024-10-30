import traceback


class SyntaxParser:
    """
    Parse the style tree into the syntax tree

    Parameters:
      style_tree: style tree of the drawio file
    """

    ACCESS_MODIFIER_MAPPINGS = {
        '+': "public",
        '#': "protected",
        '-': "private"
    }

    def __init__(self, style_tree):
        self.style_tree = style_tree

    @staticmethod
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

    @staticmethod
    def parse_member_signature(member_sig):
        member_sig = member_sig.strip()

        if member_sig.endswith('}'):
            lbrace = member_sig.find('{')
            if lbrace < 0:
                raise ValueError(f"Member signature: {member_sig}. Missing opening brace")
            else:
                constraints = [s.strip() for s in member_sig[lbrace + 1:-1].split(',') if s.strip()]
                member_sig = member_sig[:lbrace].strip()
        else:
            constraints = []

        access = member_sig[0]
        if access in SyntaxParser.ACCESS_MODIFIER_MAPPINGS.keys():
            member_sig = member_sig[1:]
        else:
            access = '-'

        return access, member_sig.split(':'), constraints

    @staticmethod
    def to_constraint_dict(constraints):
        constraint_dict = {}
        other_constraints = set()

        for constraint in constraints:
            if constraint in ("static", "virtual", "final", "required", "unique", "pk", "identity"):
                constraint_dict[constraint] = True
            elif constraint.startswith("fk:"):
                constraint_dict['fk'] = True
                constraint_dict['fk_target'] = constraint[3:]
            elif constraint.startswith("length:"):
                constraint_dict['length'] = int(constraint[7:])
            elif constraint.startswith("size:"):
                parts = constraint[5:].split(':')
                constraint_dict['size'] = (int(parts[0].strip()), int(parts[1].strip()))
            elif constraint.startswith("format:"):
                constraint_dict['format'] = constraint[7:]
            else:
                other_constraints.add(constraint)

        constraint_dict['other'] = other_constraints

        return constraint_dict

    @staticmethod
    def parse_property_signature(property_sig):
        access, parts, constraints = SyntaxParser.parse_member_signature(property_sig)
        constraint_dict = SyntaxParser.to_constraint_dict(constraints)

        if len(parts) > 1:
            name = parts[0].strip()
            parts = parts[1].split("=")
            data_type = parts[0].strip()
        else:
            data_type = 'unspecified'
            parts = parts[0].split("=")
            name = parts[0].strip()

        default_value = parts[1].strip() if len(parts) > 1 else None

        return access, name, data_type, default_value, constraint_dict

    @staticmethod
    def parse_parameter_signature(parameter_sig):
        parts = parameter_sig.split(':')

        if len(parts) > 1:
            param_name = parts[0].strip()
            param_type = parts[1].strip()
        else:
            param_name = None
            param_type = parts[0].strip()

        return {'name': param_name, 'type': param_type}

    @staticmethod
    def parse_method_signature(method_sig):
        access, parts, constraints = SyntaxParser.parse_member_signature(method_sig)
        name = parts[0].strip()
        return_type = parts[1].strip() if len(parts) > 1 else "void"
        constraint_dict = SyntaxParser.to_constraint_dict(constraints)

        if name.endswith(")"):
            lparen = name.find("(")
            if lparen < 0:
                raise ValueError(f"Malformed method signature: {method_sig}. Missing opening parenthesis")
            else:
                parameters = [SyntaxParser.parse_parameter_signature(s) for s in name[lparen + 1:-1].split(',')]
                name = name[:lparen].strip()

                for i in range(len(parameters)):
                    if not parameters[i]['name']:
                        parameters[i]['name'] = f"arg{i}"
        else:
            parameters = []

        return access, name, parameters, return_type, constraint_dict

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
                    syntax_tree[key] = self.tree_template(value)
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
                                **self.methods_template(value, _id)
                            }
                        else:  # properties
                            syntax_tree[value['parent_id']]['properties'] = {
                                **syntax_tree[value['parent_id']]['properties'],
                                **self.properties_template(value, _id)
                            }

                        _id += len(value['values'])

            for relationship in relationships.keys():
                self.add_relationships(syntax_tree, relationships[relationship])
        except Exception as e:
            print(f"SyntaxParser.convert_to_syntax_tree ERROR: {e}")
            traceback.print_exception(e)

        return syntax_tree

    def tree_template(self, main_cell):
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
            template['properties'] = self.properties_template(properties, 0) or {}
            template['methods'] = self.methods_template(methods, 0) or {}

        name, stereotype = self.parse_class_name(template['name'])
        template['name'] = name

        if stereotype in ("interface", "enum"):
            template['type'] = stereotype
        elif stereotype == "enumeration":
            template['type'] = "enum"
        elif stereotype == "abstract":
            template['type'] = "abstract class"
        else:
            template['stereotype'] = stereotype
            if main_cell['style'].get('fontStyle') == "2":  # itallic
                template['type'] = "abstract class"

        return template

    def properties_template(self, property_dict, _id):
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
                access, name, data_type, default_value, constraints = self.parse_property_signature(val)
                template[_id] = {
                    'access': self.get_access_modifier(access),
                    'name': name,
                    'type': data_type,
                    'default_value': default_value,
                    'constraints': constraints,
                }

        return template

    def methods_template(self, method_dict, _id):
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
                access, name, parameters, return_type, constraints = self.parse_method_signature(val)
                template[_id] = {
                    'access': self.get_access_modifier(access),
                    'name': name,
                    'parameters': parameters,
                    'return_type': return_type,
                    'constraints': constraints,
                }

        return template

    def get_access_modifier(self, symbol):
        """
        Return the access modifier

        Parameters:
          symbol: symbol representing the access modifier

        Returns:
          text: the text of the access modifier symbol
        """

        return self.ACCESS_MODIFIER_MAPPINGS.get(symbol, 'private')

    def add_relationships(self, syntax_tree, relationship):
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
