from pydantic import BaseModel, Field


class AlertCreate(BaseModel):
    alert_id: str = Field(min_length=1)
    severity: str = Field(min_length=1)
    category: str = Field(min_length=1)
    message: str = Field(min_length=1)


class AlertRecord(AlertCreate):
    recommendation_count: int


class RemediationRequest(BaseModel):
    alert_id: str = Field(min_length=1)


class RemediationRecommendation(BaseModel):
    action: str
    score: float


class RemediationResponse(BaseModel):
    alert_id: str
    summary: str
    recommendations: list[RemediationRecommendation]