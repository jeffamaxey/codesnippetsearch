from typing import List, Dict, Any

from code_search.function_parser.parsers.language_parser import LanguageParser, match_from_span, tokenize_code, \
    traverse_type, previous_sibling, node_parent
from code_search.function_parser.parsers.comment_utils import get_docstring_summary, strip_c_style_comment_delimiters


class JavascriptParser(LanguageParser):
    BLACKLISTED_FUNCTION_NAMES = {'toString', 'toLocaleString', 'valueOf'}

    @staticmethod
    def get_docstring(tree, node, blob: str) -> str:
        docstring = ''
        parent_node = node_parent(tree, node)

        if parent_node.type == 'variable_declarator':
            base_node = node_parent(tree, parent_node)  # Get the variable declaration
        elif parent_node.type == 'pair':
            base_node = parent_node  # This is a common pattern where a function is assigned as a value to a dictionary.
        else:
            base_node = node

        prev_sibling = previous_sibling(tree, base_node)
        if prev_sibling is not None and prev_sibling.type == 'comment':
            all_prev_comment_nodes = [prev_sibling]
            prev_sibling = previous_sibling(tree, prev_sibling)
            while prev_sibling is not None and prev_sibling.type == 'comment':
                all_prev_comment_nodes.append(prev_sibling)
                last_comment_start_line = prev_sibling.start_point[0]
                prev_sibling = previous_sibling(tree, prev_sibling)
                if prev_sibling is not None and prev_sibling.end_point[0] + 1 < last_comment_start_line:
                    break  # if there is an empty line, stop expanding.

            docstring = ' '.join(
                (strip_c_style_comment_delimiters(match_from_span(s, blob)) for s in all_prev_comment_nodes[::-1]))
        return docstring
        
    @staticmethod
    def get_definitions(tree, blob: str) -> List[Dict[str, Any]]:
        functions = []
        function_nodes = []
        traverse_type(tree.root_node, function_nodes, 'function_declaration')

        method_nodes = []
        traverse_type(tree.root_node, method_nodes, 'method_definition')

        functions.extend(
            (declaration, JavascriptParser.get_docstring(tree, declaration, blob))
            for declaration in function_nodes + method_nodes
            if declaration.children is not None and len(declaration.children) != 0
        )
        definitions = []
        for function_node, docstring in functions:
            metadata = JavascriptParser.get_function_metadata(function_node, blob)
            docstring_summary = get_docstring_summary(docstring)

            if metadata['identifier'] in JavascriptParser.BLACKLISTED_FUNCTION_NAMES:
                continue

            definitions.append({
                'identifier': metadata['identifier'],
                'parameters': metadata['parameters'],
                'function': match_from_span(function_node, blob),
                'function_tokens': tokenize_code(function_node, blob),
                'docstring': docstring,
                'docstring_summary': docstring_summary,
                'start_point': function_node.start_point,
                'end_point': function_node.end_point     
            })

        return definitions

    @staticmethod
    def get_function_metadata(function_node, blob: str) -> Dict[str, str]:
        metadata = {
            'identifier': '',
            'parameters': '',
        }
        identifier_nodes = [child for child in function_node.children
                            if child.type in ['identifier', 'property_identifier']]
        formal_parameters_nodes = [child for child in function_node.children if child.type == 'formal_parameters']
        if identifier_nodes:
            metadata['identifier'] = match_from_span(identifier_nodes[0], blob)
        if formal_parameters_nodes:
            metadata['parameters'] = match_from_span(formal_parameters_nodes[0], blob)
        return metadata
