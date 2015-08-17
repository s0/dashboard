import yaml

class Config(object):
    
    def __init__(self, config_file):
        stream = open(config_file, 'r')
        self.data = yaml.load(stream, Loader=yaml.Loader)
        
    def get(self, *path):
        current = self.data
        for section in path:
            if section in current:
                current = current[section]
            else:
                return None
        return current