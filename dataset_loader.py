"""
Dataset Loader Dinâmico para Sistema CSP
Permite carregar datasets em formato .txt de forma flexível
"""

import os
import re

class DatasetLoader:
    def __init__(self, dataset_path):
        self.dataset_path = dataset_path
        self.cc = {}  # courses assigned to classes
        self.dsd = {}  # courses assigned to lecturers
        self.tr = {}  # timeslot restrictions
        self.rr = {}  # room restrictions
        self.oc = {}  # online classes
        self.rooms = ['RoomA', 'RoomB', 'RoomC', 'Lab01', 'Online']  # default
        self.teachers = []
        self.classes = []
        self.courses = []
        
    def load_dataset(self):
        """Carrega dataset do ficheiro .txt"""
        with open(self.dataset_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self._parse_sections(content)
        self._extract_derived_data()
        return self._get_dataset_dict()
    
    def _parse_sections(self, content):
        """Parse das diferentes secções do dataset"""
        sections = {
            '#cc': self._parse_cc,
            '#dsd': self._parse_dsd,
            '#tr': self._parse_tr,
            '#rr': self._parse_rr,
            '#oc': self._parse_oc,
            '#rooms': self._parse_rooms
        }
        
        current_section = None
        for line in content.split('\n'):
            line = line.strip().replace('\r', '')  # Remove \r do Windows
            if not line or line.startswith('—') or line.startswith(' ') or line.startswith('#head') or line.startswith('#olw'):
                continue
                
            if line.startswith('#'):
                # Extrai apenas a parte da seção (antes do espaço)
                current_section = line.split()[0] if line.split() else line
                continue
                
            if current_section in sections:
                sections[current_section](line)
    
    def _parse_cc(self, line):
        """Parse courses assigned to classes"""
        parts = line.split()
        if len(parts) >= 2:
            class_name = parts[0]
            courses = parts[1:]
            self.cc[class_name] = courses
    
    def _parse_dsd(self, line):
        """Parse courses assigned to lecturers"""
        parts = line.split()
        if len(parts) >= 2:
            teacher = parts[0]
            courses = parts[1:]
            self.dsd[teacher] = courses
    
    def _parse_tr(self, line):
        """Parse timeslot restrictions"""
        parts = line.split()
        if len(parts) >= 2:
            teacher = parts[0]
            slots = [int(slot) for slot in parts[1:]]
            self.tr[teacher] = slots
    
    def _parse_rr(self, line):
        """Parse room restrictions"""
        parts = line.split()
        if len(parts) == 2:
            course, room = parts
            self.rr[course] = room
    
    def _parse_oc(self, line):
        """Parse online classes"""
        parts = line.split()
        if len(parts) == 2:
            course, lesson_idx = parts
            self.oc[course] = int(lesson_idx)
    
    def _parse_rooms(self, line):
        """Parse available rooms"""
        if line.strip():
            if not hasattr(self, '_custom_rooms'):
                self._custom_rooms = []
            self._custom_rooms.append(line.strip())
    
    def _extract_derived_data(self):
        """Extrai dados derivados dos dados principais"""
        self.teachers = list(self.dsd.keys())
        self.classes = list(self.cc.keys())
        
        # Remove duplicatas de cursos (UCs partilhadas entre turmas)
        all_courses = [course for courses_list in self.cc.values() for course in courses_list]
        self.courses = list(set(all_courses))  # Remove duplicatas
        
        # Usa salas customizadas se definidas, senão usa default + Online
        if hasattr(self, '_custom_rooms'):
            self.rooms = self._custom_rooms + ['Online']
    
    def _get_dataset_dict(self):
        """Retorna dicionário com todos os dados do dataset"""
        return {
            'cc': self.cc,
            'dsd': self.dsd,
            'tr': self.tr,
            'rr': self.rr,
            'oc': self.oc,
            'rooms': self.rooms,
            'teachers': self.teachers,
            'classes': self.classes,
            'courses': self.courses
        }

def load_dataset_from_file(dataset_path):
    """Função utilitária para carregar dataset"""
    loader = DatasetLoader(dataset_path)
    return loader.load_dataset()

def list_available_datasets(material_folder='material'):
    """Lista datasets disponíveis na pasta material"""
    datasets = []
    if os.path.exists(material_folder):
        for file in os.listdir(material_folder):
            if file.endswith('.txt'):
                datasets.append(os.path.join(material_folder, file))
    return datasets