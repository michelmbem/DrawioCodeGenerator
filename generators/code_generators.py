from generators.ts_generator import TsCodeGenerator
from generators.java_generator import JavaCodeGenerator
from generators.csharp_generator import CSharpCodeGenerator
from generators.cpp_generator import CppCodeGenerator
from generators.php_generator import PhpCodeGenerator
from generators.python_generator import PythonCodeGenerator
from generators.sql_generator import SqlCodeGenerator


class CodeGenerators:
    """
    Collection of factory methods for the CodeGeneratorInterface
    """

    @staticmethod
    def create(language, syntax_tree, output_dir):
        """
        Creates an instance of a class that implements the CodeGeneratorInterface for the given language.
        :param language: The name of the language for which to generate a code generator
        :param syntax_tree: The abstract syntax tree
        :param output_dir: The target output directory
        :return: An instance of a class that implements the CodeGeneratorInterface
        """

        language = language.lower()

        if language == "ts" or language == "typescript":
            code_gen = TsCodeGenerator(syntax_tree, output_dir)
        elif language == "java":
            code_gen = JavaCodeGenerator(syntax_tree, output_dir)
        elif language == "c#" or language == "cs" or language == "csharp" or language == "c-sharp":
            code_gen = CSharpCodeGenerator(syntax_tree, output_dir)
        elif language == "c++" or language == "cpp" or language == "cplusplus":
            code_gen = CppCodeGenerator(syntax_tree, output_dir)
        elif language == "php":
            code_gen = PhpCodeGenerator(syntax_tree, output_dir)
        elif language == "python":
            code_gen = PythonCodeGenerator(syntax_tree, output_dir)
        elif language == "sql":
            code_gen = SqlCodeGenerator(syntax_tree, output_dir)
        else:
            raise ValueError(f"{language} language is not supported for code generation")

        return code_gen
