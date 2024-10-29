from generators.java_generator import JavaCodeGenerator
from generators.csharp_generator import CSharpCodeGenerator
from generators.cpp_generator import CppCodeGenerator
from generators.python_generator import PythonCodeGenerator
from generators.ts_generator import TsCodeGenerator
from generators.php_generator import PhpCodeGenerator
from generators.sql_generator import SqlCodeGenerator


class CodeGenerators:
    """
    Collection of factory methods for code generators
    """

    LANGUAGE_MAPPINGS = {
        'java': "java",
        'c#': "cs",
        'cs': "cs",
        'csharp': "cs",
        'c-sharp': "cs",
        'c++': "cpp",
        'cpp': "cpp",
        'cplusplus': "cpp",
        'c-plus-plus': "cpp",
        'python': "python",
        'ts': "ts",
        'typescript': "ts",
        'php': "php",
        'sql': "sql",
    }

    LANGUAGE_NAMES = {
        'java': "Java",
        'cs': "C#",
        'cpp': "C++",
        'python': "Python",
        'ts': "TypeScript",
        'php': "PHP",
        'sql': "SQL",
    }

    @staticmethod
    def get(language, syntax_tree, output_dir, options):
        """
        Creates an instance of a class that extends CodeGenerator for the given language.

        :param language: The language for which to generate a code generator
        :param syntax_tree: An abstract syntax tree
        :param output_dir: The target output directory
        :param options: Set of code generation options

        :return: An instance of a subclass of CodeGenerator
        """

        language_code = CodeGenerators.language_code(language)
        language_options = CodeGenerators.extract_language_options(options, language_code)

        if language_code == "java":
            code_gen = JavaCodeGenerator(syntax_tree, output_dir, language_options)
        elif language_code == "cs":
            code_gen = CSharpCodeGenerator(syntax_tree, output_dir, language_options)
        elif language_code == "cpp":
            code_gen = CppCodeGenerator(syntax_tree, output_dir, language_options)
        elif language_code == "python":
            code_gen = PythonCodeGenerator(syntax_tree, output_dir, language_options)
        elif language_code == "ts":
            code_gen = TsCodeGenerator(syntax_tree, output_dir, language_options)
        elif language_code == "php":
            code_gen = PhpCodeGenerator(syntax_tree, output_dir, language_options)
        elif language_code == "sql":
            code_gen = SqlCodeGenerator(syntax_tree, output_dir, language_options)
        else:
            raise ValueError(f"Could not find a code generator for the '{language}' language")

        return code_gen

    @staticmethod
    def language_code(language_name):
        return CodeGenerators.LANGUAGE_MAPPINGS.get(language_name.lower())

    @staticmethod
    def language_name(language_code):
        return CodeGenerators.LANGUAGE_NAMES.get(language_code, language_code)

    @staticmethod
    def extract_language_options(options, language_code):
        language_options = {**options, **options['language_specific'][language_code]}
        del language_options['language_specific']
        return language_options
