from enum import Enum
class ReviewStatus(Enum):
    DRAFT = 'draft'
    IN_REVIEW = 'in_review'
    DEACCESSIONED = 'deaccessioned'
    PUBLISHED = 'published'
