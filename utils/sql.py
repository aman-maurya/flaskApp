class SqlUtils:

    @classmethod
    def rows_as_dict(cls, results):
        return [cls.to_dict(row) for row in results]

    @classmethod
    def to_dict(cls, row):
        return (lambda r: {c.name: str(getattr(r, c.name)) for c in r.__table__.columns})(row)
