from src.models import AlertCreate, AlertRecord, RemediationRecommendation, RemediationResponse


def _severity_weight(severity: str) -> float:
    mapping = {"critical": 1.0, "high": 0.8, "medium": 0.5, "low": 0.3}
    return mapping.get(severity.lower(), 0.4)


class AlertStore:
    def __init__(self) -> None:
        self._alerts: dict[str, AlertCreate] = {}

    def add_alert(self, payload: AlertCreate) -> AlertRecord:
        self._alerts[payload.alert_id] = payload
        return AlertRecord(**payload.model_dump(), recommendation_count=3)

    def get_alert(self, alert_id: str) -> AlertRecord | None:
        alert = self._alerts.get(alert_id)
        if alert is None:
            return None
        return AlertRecord(**alert.model_dump(), recommendation_count=3)

    def remediate(self, alert_id: str) -> RemediationResponse:
        alert = self._alerts.get(alert_id)
        if alert is None:
            return RemediationResponse(alert_id=alert_id, summary="No alert found.", recommendations=[])

        base_score = _severity_weight(alert.severity)
        recommendations = [
            RemediationRecommendation(action=f"Investigate {alert.category} pipeline health", score=round(base_score, 2)),
            RemediationRecommendation(action="Check observability dashboards and recent deploys", score=round(max(base_score - 0.1, 0.1), 2)),
            RemediationRecommendation(action="Trigger rollback or safe-mode if error rate persists", score=round(max(base_score - 0.2, 0.1), 2)),
        ]
        return RemediationResponse(
            alert_id=alert.alert_id,
            summary=f"Automated guidance for {alert.severity.lower()} {alert.category} alert.",
            recommendations=recommendations,
        )