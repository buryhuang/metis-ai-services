"""Class definition for DataSet model."""
from sqlalchemy import Column, String

# from metis_ai_services import db
from flask_sqlalchemy import Model


class DataFrame(Model):
    """DataFrame model for a generic resource in a REST API."""

    __tablename__ = "dataframe"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    uri = Column(String(255), nullable=False)
    ds_id = Column(String(64), nullable=False)
    description = Column(String(255), nullable=False)

    # owner_id = Column(String(64), ForeignKey("site_user.id"), nullable=False)
    # owner = db.relationship("User", backref=db.backref("widgets"))

    def __repr__(self):
        return f"<DataSet id={self.id}, \
                          name={self.name}, \
                          uri={self.uri}, \
                          ds_id={self.ds_id}, \
                          description={self.description}>"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ds_id": self.ds_id,
            "uri": self.uri,
        }
