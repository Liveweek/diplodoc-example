import ast
import os
from dataclasses import dataclass


@dataclass
class ApiReference:
    module_name: str
    module_description: str
    generated_documentation: str


api_reference_pool: list[ApiReference] = []

MODULE_PATTERN = """
# {module_name}
{module_documentation}

{class_def_docs}
""".strip()

CLASSDEF_PATTERN = """
## *{class_name}*
*{class_description}*

{class_attr}

{public_methods}
""".strip()

FUNCDEF_PATTERN = """
***##{method_name}({arguments})##***

{method_doc}

Аргументы:
{arg_list}
""".strip()

TOC_PATTERN = """
title: API-документация
href: index.yaml
items:
{modules}
""".strip()

INDEX_PATTERN = """
title: API-Документация
links:
{links}
""".strip()


def get_source_files(target_path: str):
    for file_name in os.listdir(target_path):
        if not file_name.startswith("__init__"):
            with open(target_path + file_name) as file:
                yield file_name, file.read()


def make_class_attr_reference(annotation: ast.AnnAssign) -> str:
    field_name = annotation.target.id
    if isinstance(annotation.annotation, ast.Name):
        annotated_type = annotation.annotation.id
    elif isinstance(annotation.annotation, ast.Subscript):
        annotated_type = f"{annotation.annotation.value.id}[{annotation.annotation.slice.id}]"
    elif isinstance(annotation.annotation, ast.Attribute):
        annotated_type = f"{annotation.annotation.value.id}.{annotation.annotation.attr}"
    return f"- `{field_name}`: `{annotated_type}`"


def make_class_method_reference(
    class_name: str,
    func_def: ast.FunctionDef
) -> str:
    method_name = f"{class_name}.{func_def.name}"
    print("METHOD: ", method_name)
    method_doc = func_def.body[0].value.value.strip()
    # print(ast.dump(func_def, indent=4))
    args = [arg for arg in func_def.args.args]
    return FUNCDEF_PATTERN.format(
        method_name=method_name,
        arguments=', '.join([arg.arg for arg in args]),
        method_doc=method_doc,
        arg_list='\n'.join([f"- `{arg.arg}`" for arg in args])
    )


def make_class_def_reference(class_def: ast.ClassDef) -> str:
    class_name = class_def.name
    print("CLASS: ", class_name)
    class_doc = class_def.body[0].value.value.strip()

    annotated_attrs = [
        node for node in class_def.body
        if isinstance(node, ast.AnnAssign) and node.target.id != '_'
    ]
    class_attrs_doc = [
        make_class_attr_reference(attr)
        for attr in annotated_attrs
    ]

    class_func_defs = [
        node for node in class_def.body
        if isinstance(node, ast.FunctionDef) and not node.name.startswith("_")
    ]
    public_methods_doc = [
        make_class_method_reference(class_name, func_def)
        for func_def in class_func_defs
    ]

    return CLASSDEF_PATTERN.format(
        class_name=class_name,
        class_description=class_doc,
        class_attr="**Атрибуты класса**\n\n" + "\n\n".join(class_attrs_doc) if class_attrs_doc else "",
        public_methods="**Публичные методы класса**\n\n" + "\n\n".join(public_methods_doc) if public_methods_doc else ""
    )


def make_api_reference(file_name: str, source_code: str) -> ApiReference:
    module_ast = ast.parse(source_code)

    module_name = file_name.split('.')[0]
    module_description = module_ast.body[0].value.value

    return ApiReference(
        module_name=module_name,
        module_description=module_description,
        generated_documentation=MODULE_PATTERN.format(
            module_name=module_name.capitalize(),
            module_documentation=module_description,
            class_def_docs='\n\n'.join(
                make_class_def_reference(class_def)
                for class_def in module_ast.body if isinstance(class_def, ast.ClassDef)
            )
        )
    )


def write_doc_via_api_reference(target_path: str, api_reference: ApiReference):
    full_path = target_path + api_reference.module_name + '.md'
    with open(full_path, 'w') as f:
        f.write(api_reference.generated_documentation)


def write_toc_and_index_yaml(target_path: str, api_ref_pool: list[ApiReference]):
    toc_file_path = target_path + 'toc.yaml'
    index_file_path = target_path + 'index.yaml'

    with open(toc_file_path, 'w') as f:
        f.write(TOC_PATTERN.format(
            modules="\n".join([
                f" - name: {api_ref.module_name.capitalize()}\n   href: {api_ref.module_name}.md"
                for api_ref in api_ref_pool
            ])
        ))

    with open(index_file_path, 'w') as f:
        f.write(INDEX_PATTERN.format(
            links="\n".join(
                f" - title: {api_ref.module_name.capitalize()}\n   href: {api_ref.module_name}.md"
                for api_ref in api_ref_pool
            )
        ))

if __name__ == "__main__":
    for file_name, src in get_source_files("code_core/"):
        api_ref = make_api_reference(file_name, src)
        api_reference_pool.append(api_ref)
        write_doc_via_api_reference('docs/api-reference/', api_ref)
    write_toc_and_index_yaml('docs/api-reference/', api_reference_pool)
