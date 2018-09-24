import os
import pickle
from datastorage.LabelStorage import LabelManager
from datastorage.SubjectMapping import SubjectManager


settings_file_name = "settings.pkl"


def new_project(project_name):
    if not os.path.exists('projects/' + project_name):
        os.mkdir('projects/' + project_name)
        Settings(project_name, True)
        LabelManager(project_name).create_tables()
        SubjectManager(project_name).create_table()


class Settings:

    settings_dict = {}

    def __init__(self, project_name, is_new_project=False):
        self.project_name = project_name
        if is_new_project:
            self.save()
        else:
            self.load()

    def load(self):
        """Loads the saved values back into this class from a file"""
        f = open(self._get_path(), 'rb')
        self.settings_dict = pickle.load(f)
        f.close()

    def save(self):
        """Saves the values inside this class to a file"""
        f = open(self._get_path(), 'wb')
        pickle.dump(self.settings_dict, f)
        f.close()

    def set_setting(self, setting_name, new_value):
        self.settings_dict[setting_name] = new_value
        self.save()

    def get_setting(self, setting_name):
        return self.settings_dict[setting_name]

    def _get_path(self):
        return 'projects/' + self.project_name + '/' + settings_file_name
