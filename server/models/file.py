from server.extensions import db
from server.models.mixin import TimestampMixin
from sqlalchemy.dialects.postgresql import UUID


class File(db.Model, TimestampMixin):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    data = db.Column(db.LargeBinary)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey("users.id", ondelete="CASCADE"))

    def __init__(self, *args, **kwargs):
        super(File, self).__init__(*args, **kwargs)
