from enum import Enum
from typing import List
from pydantic import BaseModel, Field


class AccessModel(str, Enum):
    SELF_SERVE_FREE = "self_serve_free"
    SELF_SERVE_TRIAL = "self_serve_trial"
    PAID_PLAN_REQUIRED = "paid_plan_required"
    ADMIN_APPROVAL = "admin_approval"
    PARTNER_APPROVAL = "partner_approval"
    CONTACT_SALES = "contact_sales"
    UNKNOWN = "unknown"


class APIBreadth(str, Enum):
    NARROW = "narrow"
    MODERATE = "moderate"
    BROAD = "broad"
    UNKNOWN = "unknown"


class Buildability(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    UNKNOWN = "unknown"


class VerificationStatus(str, Enum):
    UNVERIFIED = "unverified"
    VERIFIED = "verified"
    NEEDS_REVIEW = "needs_review"
    CONTRADICTED = "contradicted"


class Evidence(BaseModel):

    claim: str

    url: str

    source_type: str = Field(
        description=(
            "official_docs, official_website, "
            "official_github, or secondary_source"
        )
    )

class PrimaryBlocker(str, Enum):

    NONE = "none"

    NO_PUBLIC_API = "no_public_api"

    PAID_ACCESS = "paid_access"

    ADMIN_APPROVAL = "admin_approval"

    PARTNER_GATE = "partner_gate"

    CONTACT_SALES = "contact_sales"

    LIMITED_API = "limited_api"

    AUTH_COMPLEXITY = "auth_complexity"

    RATE_LIMITS = "rate_limits"

    UNCLEAR_DOCUMENTATION = "unclear_documentation"

    UNKNOWN = "unknown"


class AppResearchResult(BaseModel):

    id: int

    app_name: str

    category: str

    description: str

    auth_methods: List[str]

    access_model: AccessModel

    access_notes: str

    api_types: List[str]

    api_breadth: APIBreadth

    existing_mcp: bool

    mcp_type: str

    mcp_notes: str

    buildability: Buildability

    primary_blocker: PrimaryBlocker

    evidence: List[Evidence]

    confidence_score: float = Field(
        ge=0,
        le=1
    )

    verification_status: VerificationStatus = (
        VerificationStatus.UNVERIFIED
    )

    research_attempts: int = 1

    human_verified: bool = False

class ClaimVerification(BaseModel):
    claim: str

    url: str

    status: str = Field(
        description="supported, contradicted, or insufficient"
    )

    explanation: str

    confidence: float = Field(
        ge=0,
        le=1
    )


class VerificationResult(BaseModel):
    app_id: int

    app_name: str

    claim_verifications: List[ClaimVerification]

    evidence_coverage_score: float = Field(
        ge=0,
        le=1
    )

    source_quality_score: float = Field(
        ge=0,
        le=1
    )

    verifier_agreement_score: float = Field(
        ge=0,
        le=1
    )

    final_confidence_score: float = Field(
        ge=0,
        le=1
    )

    verification_status: VerificationStatus

    verification_notes: str