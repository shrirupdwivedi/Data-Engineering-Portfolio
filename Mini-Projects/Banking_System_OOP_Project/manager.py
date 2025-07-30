


class manager():
    """
    class manager() is created to initialize and store SQLite database named Customer and execute basic SQLite functions.
    """


    def __init__(self):
    
        import sqlalchemy as db
        import logging
  
        #create database in SQLite
        engine = db.create_engine('sqlite:///test.sqlite')
        self.connection = engine.connect()
        metadata = db.MetaData()


        self.Customer = db.Table('Customer', metadata,
                            db.Column('acc_no', db.Integer(), primary_key=True,
                                    nullable=False, autoincrement=True),
                            db.Column('first_name', db.String(255), nullable=False),
                            db.Column('last_name', db.String(255)),
                            db.Column('dob', db.Integer()),
                            db.Column('email', db.String(255)),
                            db.Column('acc_type', db.String(255)),
                            db.Column('status', db.String(255)),
                            db.Column('balance', db.Integer())

                            )

        metadata.create_all(engine)  # Creates the table

        # Creates a logger
        self.logger = logging.getLogger(__name__)

        # set logger level
        self.logger.setLevel(logging.DEBUG)

        # define file handler and set formatter
        file_handler = logging.FileHandler('Bank.log')
        formatter = logging.Formatter('%(asctime)s : %(levelname)s : %(name)s : %(message)s')
        file_handler.setFormatter(formatter)

        # add file handler to logger
        self.logger.addHandler(file_handler)

    #SQLite functions
    def execute(self, query):
        return self.connection.execute(query)

    def fetchall(self, query):
        return self.connection.execute(query).fetchall()

    def fetchone(self, query):
        return self.connection.execute(query).fetchone()
