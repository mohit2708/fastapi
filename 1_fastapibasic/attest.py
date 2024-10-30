class User(Base):
    __table__ = "users"
    __table_args = ( {'schema':'employee'} ) # in postgresql it is schema but in mysql it is database name
