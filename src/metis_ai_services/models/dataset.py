"""Class definition for DataSet model."""
from datetime import datetime, timezone, timedelta
from sqlalchemy import Column, String, DateTime

# from sqlalchemy.orm import relationship
# from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.hybrid import hybrid_property
from metis_ai_services import db
from metis_ai_services.utils.datetime_util import (
    utc_now,
    format_timedelta_str,
    get_local_utcoffset,
    localized_dt_string,
    make_tzaware,
)
from metis_ai_services.utils.sql_util import dump_datetime


class DataSet(db.Model):
    """DataSet model for a generic resource in a REST API."""

    __tablename__ = "dataset"

    id = Column(String(64), primary_key=True)
    name = Column(String(128), unique=True, nullable=False)
    description = Column(String(255))
    created_at = Column(DateTime, default=utc_now)
    owner_id = Column(String(64), nullable=False)
    image_url = Column(String(255), nullable=False)
    # owner_id = Column(String(64), ForeignKey("site_user.id"), nullable=False)
    # owner = db.relationship("User", backref=db.backref("widgets"))

    def __repr__(self):
        return f"<DataSet id={self.id}, \
                          name={self.name}, \
                          description={self.description}, \
                          created_at={self.created_at}, \
                          owner_id={self.owner_id}, \
                          image_url={self.image_url}>"

    @property
    def serialize(self):
        """Return object data in easily serializable format"""
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "created_at": dump_datetime(self.created_at),
            "owner_id": self.owner_id,
            "image_url": self.image_url,
        }

    @hybrid_property
    def created_at_str(self):
        created_at_utc = make_tzaware(self.created_at, use_tz=timezone.utc, localize=False)
        return localized_dt_string(created_at_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def deadline_str(self):
        deadline_utc = make_tzaware(self.deadline, use_tz=timezone.utc, localize=False)
        return localized_dt_string(deadline_utc, use_tz=get_local_utcoffset())

    @hybrid_property
    def deadline_passed(self):
        return datetime.now(timezone.utc) > self.deadline.replace(tzinfo=timezone.utc)

    @hybrid_property
    def time_remaining(self):
        time_remaining = self.deadline.replace(tzinfo=timezone.utc) - utc_now()
        return time_remaining if not self.deadline_passed else timedelta(0)

    @hybrid_property
    def time_remaining_str(self):
        timedelta_str = format_timedelta_str(self.time_remaining)
        return timedelta_str if not self.deadline_passed else "No time remaining"

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
