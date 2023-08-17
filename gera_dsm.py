import os
from plyj.parser import Parser
import numpy as np
import logging

class JavaFileAnalyzer:
    def __init__(self, repo_folder, dsm_filename):
        self.repo_folder = repo_folder
        self.java_files = []
        self.dependency_matrix = {}
        self.dsm_filename = dsm_filename
        self.all_classes = []
        self.parser = Parser()

        # Configure logging
        self.log_file = 'JavaFileAnalyzer_error_log.txt'
        logging.basicConfig(filename=self.log_file, level=logging.ERROR,
                            format='%(asctime)s - %(levelname)s - %(message)s')

    
    def find_java_files(self):
        for root, dirs, files in os.walk(self.repo_folder):
            for file in files:
                if file.endswith(".java"):
                    self.java_files.append(os.path.join(root, file))

    def collect_class_names(self):
        for java_file in self.java_files:
            with open(java_file, "r") as file:
                content = file.read()
                try:
                    tree = self.parser.parse_string(content)
                    if tree is not None: 
                        for type_declaration in tree.type_declarations:
                            if type_declaration is not None:
                                if hasattr(type_declaration, 'name') and type_declaration.name is not None:
                                    self.all_classes.append(type_declaration)
                                    print(str(type_declaration.name))
                                    if type_declaration.extends is not None:
                                        print(' -> extending ' + type_declaration.extends.name)
                                    if len(type_declaration.implements) is not 0:
                                        print(' -> implementing ' + ', '.join([type.name for type in type_declaration.implements]))
                except Exception as e:
                    logging.error(f"Error parsing {java_file}: {e}")
    
    def analyze_dependencies(self):
        for java_file in self.java_files:
            with open(java_file, "r") as file:
                content = file.read()
                try:
                    tree = self.parser.parse_string(content)
                    imports = [imp.name.value for imp in tree.import_declarations]

                    for type_declaration in tree.type_declarations:
                        if hasattr(type_declaration, 'name') and type_declaration.name:
                            type_name = type_declaration.name
                            self.dependency_matrix[type_name] = imports
                except Exception as e:
                    logging.error(f"Error parsing {java_file}: {e}")

    def generate_dsm(self):
        all_types = set(self.dependency_matrix.keys())
        for dependencies in self.dependency_matrix.values():
            all_types.update(dependencies)
        
        num_types = len(all_types)
        matrix = np.zeros((num_types, num_types), dtype=int)
        type_index_mapping = {type_name: index for index, type_name in enumerate(all_types)}
        lista_types = list(type_index_mapping.keys())
        
        for type_name, imports in self.dependency_matrix.items():
            type_index = type_index_mapping[type_name]
            for dependency in imports:
                dependency_index = type_index_mapping.get(dependency, -1)
                if dependency_index != -1:
                    matrix[type_index, dependency_index] = 1
        
        with open(self.dsm_filename, mode='w') as f:
            for i in range(0, len(matrix)):
                for j in range(0, len(matrix)):
                    if matrix[i, j] == 1:
                        conteudo = f'{lista_types[i]}, {lista_types[j]}, {matrix[i, j]}'
                        conteudo = conteudo + '\n'
                        f.write(conteudo)
