from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone

class DisposalRecommendation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index = True, default = lambda: datetime.now(timezone.utc))
    bucket: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    filename: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    gVision_labels: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    gtp_selected_label: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64)) # null for "I don't know" 
    label_correction:so.Mapped[Optional[str]] = so.mapped_column(sa.String(64)) #null for no correction (user validated proposal)
    disposal_guidance: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    disposal_guidance_correction: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255)) #null for no correction (user validated proposal)

    def __repr__(self):
        return '<DisposalRecommendation id {}>'.format(self.id)


    