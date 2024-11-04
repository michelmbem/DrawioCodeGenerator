import traceback

from operator import itemgetter


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

    CONSTRAINT_MAPPINGS = {
        'sealed': "final",
        'const': "final",
        'readonly': "final",
        'notnull': "required",
        'nonnull': "required",
        'key': "pk",
        'id': "identity",
        'computed': "generated",
        'counter': "identity",
        'serial': "identity",
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
            if constraint in ("static", "abstract", "virtual", "final", "required",
                              "unique", "pk", "identity", "generated", "lob"):
                constraint_dict[constraint] = True
            elif constraint in ("sealed", "const", "readonly", "notnull", "nonnull",
                                "key", "id", "computed", "counter", "serial"):
                constraint_dict[SyntaxParser.CONSTRAINT_MAPPINGS[constraint]] = True
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
                parameters = [SyntaxParser.parse_parameter_signature(s) for s in name[lparen + 1:-1].split(',') if s.strip()]
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
            get_item = itemgetter('id', 'cells', 'relationships')
            root_id, cells, relationships = get_item(self.style_tree['root'])

            properties_done = False
            child_id = 0

            for key, value in cells.items():
                parent_id, style = value['parent_id'], value['style']

                # skip the label for relationships
                if parent_id in relationships.keys() or "endArrow" in style.keys():
                    continue

                style_type = style['type'].lower()

                if parent_id == root_id and style_type in ('swimlane', 'html', 'text'):
                    # start of a new cell
                    syntax_tree[key] = self.tree_template(value)
                    properties_done = False
                    child_id = 0
                elif style_type == 'line' and parent_id in syntax_tree.keys():
                    # line separating the properties and methods
                    properties_done = True
                    child_id = 0
                elif properties_done:
                    # methods
                    syntax_tree[parent_id]['methods'].update(self.methods_template(value, child_id))
                    child_id += len(value['values'])
                else:
                    # properties
                    syntax_tree[parent_id]['properties'].update(self.properties_template(value, child_id))
                    child_id += len(value['values'])

            for relationship in relationships.keys():
                self.add_relationships(syntax_tree, relationships[relationship])
        except Exception as e:
            print(f"{self.__class__.__name__}.convert_to_syntax_tree ERROR: {e}")
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
                'composition': [],
            }
        }

        if main_cell['style']['type'] in ("html", "text"):
            main_cell_values = main_cell['values']
            value_count = len(main_cell_values)
            name = main_cell_values[0] if value_count > 0 else ""
            properties = {'values': main_cell_values[1] if value_count > 1 else None}
            methods = {'values': main_cell_values[2] if value_count > 2 else None}

            template['name'] = name[0]
            template['properties'] = self.properties_template(properties, 0) or {}
            template['methods'] = self.methods_template(methods, 0) or {}

        name, stereotype = self.parse_class_name(template['name'])
        template['name'] = name

        match stereotype:
            case "interface" | "enum":
                template['type'] = stereotype
            case "enumeration":
                template['type'] = "enum"
            case "abstract":
                template['type'] = "abstract class"
            case _:
                template['stereotype'] = stereotype
                if main_cell['style'].get('fontStyle') == "2":  # itallic
                    template['type'] = "abstract class"

        return template

    def properties_template(self, property_dict, property_id):
        """
        Create the template for properties

        Parameters:
          property_dict: the properties dictionary from the style tree
          property_id: id for the keys in the dictionary

        Returns:
          template: the properties template (dictionary)
        """

        values = property_dict['values']
        template = {}

        if values:
            for value in values:
                if len(value) == 0:
                    continue

                property_id += 1
                access, name, data_type, default_value, constraints = self.parse_property_signature(value)
                template[property_id] = {
                    'access': self.get_access_modifier(access),
                    'name': name,
                    'type': data_type,
                    'default_value': default_value,
                    'constraints': constraints,
                }

        return template

    def methods_template(self, method_dict, method_id):
        """
        Create the template for methods

        Parameters:
          method_dict: the methods dictionary from the style tree
          method_id: id for the keys in the dictionary

        Returns:
          template: the methods template (dictionary)
        """

        values = method_dict['values']
        template = {}

        if values:
            for value in values:
                if len(value) == 0:
                    continue

                method_id += 1
                access, name, parameters, return_type, constraints = self.parse_method_signature(value)
                template[method_id] = {
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

        get_item = itemgetter('source', 'target', 'style')
        source, target, style = get_item(relationship)

        source_cell = syntax_tree[source]
        source_relations = source_cell['relationships']

        target_cell = syntax_tree[target]
        target_relations = target_cell['relationships']

        start_arrow_style = style.get("startArrow", "").lower()
        end_arrow_style = style.get("endArrow", "").lower()
        start_arrow_filled = style.get("startFill") == "1"
        end_arrow_filled = style.get("endFill") == "1"
        dashed_line = style.get("dashed") == "1"

        match end_arrow_style:
            case "none":
                # association
                source_relations['association'].append(('to', target))
                target_relations['association'].append(('from', source))
            case "block":
                if end_arrow_filled:
                    # association
                    source_relations['association'].append(('to', target))
                    target_relations['association'].append(('from', source))
                elif dashed_line:
                    # implements
                    source_relations['implements'].append(target)
                else:
                    # extends
                    source_relations['extends'].append(target)
            case "diamondthin":
                if end_arrow_filled:
                    # composition
                    source_relations['composition'].append(('to', target))
                    target_relations['composition'].append(('from', source))
                else:
                    # aggregation
                    source_relations['aggregation'].append(('to', target))
                    target_relations['aggregation'].append(('from', source))
            case "open":
                match start_arrow_style:
                    case "diamondthin":
                        if start_arrow_filled:
                            # composition
                            source_relations['composition'].append(('to', target))
                            target_relations['composition'].append(('from', source))
                        else:
                            # aggregation
                            source_relations['aggregation'].append(('to', target))
                            target_relations['aggregation'].append(('from', source))
