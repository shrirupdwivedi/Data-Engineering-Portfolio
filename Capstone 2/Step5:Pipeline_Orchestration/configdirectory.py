from configparser import RawConfigParser

class ConfigDirectory:
    """
    ConfigDirectory class is used to parse throught the ini files to get the configuration by using
    configparser module.
    """
    def __init__(self, filename, section):
        """
        :param filename: str
                     The name of config file
        :param section: str
                     The name of section
        """
        self.filename = filename
        self.section = section
    
    def config_directory(self):
        """
        the method is used to parse through the ini files which are stored in "dbfs:/init/" directory in order to obtain the configuration
        
        :return: the configuration dictionary
        
        """
        # create a parser
        parser = RawConfigParser()
        # read config file
        parser.read("/dbfs/init/"+ self.filename)

        # get section, default to postgresql
        db = {}
        if parser.has_section(self.section):
            params = parser.items(self.section)
            for param in params:
                db[param[0]] = param[1]
        else:
            raise Exception('Section {0} not found in the {1} file'.format(self.section, self.filename))

        return db