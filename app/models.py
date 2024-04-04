from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from app import db
from datetime import datetime, timezone

class DisposalRecommendation(db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key = True)
    timestamp: so.Mapped[datetime] = so.mapped_column(index = True, default = lambda: datetime.now(timezone.utc))
    bucket: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    file_uri: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64))
    gVision_labels: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255))
    gtp_selected_label: so.Mapped[Optional[str]] = so.mapped_column(sa.String(64)) # null for "I don't know" 
    label_correction:so.Mapped[Optional[str]] = so.mapped_column(sa.String(64)) #null for no correction (user validated proposal)
    disposal_guidance: so.Mapped[Optional[str]] = so.mapped_column(sa.String(400))
    disposal_guidance_correction: so.Mapped[Optional[str]] = so.mapped_column(sa.String(255)) #null for no correction (user validated proposal)

    def __repr__(self):
        return '<DisposalRecommendation id {}>'.format(self.id)
    
    def print_all(self):
        print('Printing DisposalRecommendation with id: {}'.format(self.id))
        print('timestamp: {}'.format(self.timestamp))
        print('bucket: {}'.format(self.bucket))
        print('file_uri: {}'.format(self.file_uri))
        print('gVision_labels: {}'.format(self.gVision_labels))
        print('gtp_selected_label: {}'.format(self.gtp_selected_label))
        print('label_correction: {}'.format(self.label_correction))
        print('disposal_guidance: {}'.format(self.disposal_guidance))
        print('disposal_guidance_correction: {}'.format(self.disposal_guidance_correction))
        print("-------")
        return