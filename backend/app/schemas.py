from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


# ============ Auth Schemas ============

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    full_name: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: UUID
    exp: datetime


class UserResponse(BaseModel):
    id: UUID
    email: str
    full_name: Optional[str]
    plan: str
    currency: str
    theme: str
    created_at: datetime

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse


# ============ Account Schemas ============

class AccountCreate(BaseModel):
    name: str = Field(max_length=100)
    institution: Optional[str] = None
    account_type: str = "bank"
    current_balance: Decimal = Decimal("0")
    currency: str = "INR"


class AccountUpdate(BaseModel):
    name: Optional[str] = None
    institution: Optional[str] = None
    current_balance: Optional[Decimal] = None
    is_hidden: Optional[bool] = None


class AccountResponse(BaseModel):
    id: UUID
    name: str
    institution: Optional[str]
    account_type: Optional[str]
    current_balance: Decimal
    currency: str
    connection_type: str
    last_synced_at: Optional[datetime]
    sync_status: str
    created_at: datetime

    class Config:
        from_attributes = True


class AccountListResponse(BaseModel):
    accounts: List[AccountResponse]
    total: int
    by_type: dict


# ============ Transaction Schemas ============

class TransactionCreate(BaseModel):
    account_id: UUID
    amount: Decimal
    transaction_type: str  # credit, debit, transfer
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    category_id: Optional[int] = None
    transaction_date: datetime


class TransactionUpdate(BaseModel):
    description: Optional[str] = None
    merchant_name: Optional[str] = None
    category_id: Optional[int] = None
    tags: Optional[List[str]] = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    icon: Optional[str]

    class Config:
        from_attributes = True


class TransactionResponse(BaseModel):
    id: UUID
    account_id: UUID
    account_name: Optional[str] = None
    amount: Decimal
    transaction_type: Optional[str]
    description: Optional[str]
    merchant_name: Optional[str]
    category: Optional[CategoryResponse]
    transaction_date: datetime
    is_recurring: bool
    created_at: datetime

    class Config:
        from_attributes = True


class TransactionListResponse(BaseModel):
    transactions: List[TransactionResponse]
    total: int
    limit: int
    offset: int


class TransactionStats(BaseModel):
    total_income: Decimal
    total_expenses: Decimal
    net_cash_flow: Decimal
    by_category: List[dict]
    top_merchants: List[dict]


# ============ Asset Schemas ============

class AssetCreate(BaseModel):
    name: str = Field(max_length=100)
    asset_type: str  # real_estate, vehicle, gold, collectible, other
    current_value: Decimal
    purchase_value: Optional[Decimal] = None
    purchase_date: Optional[datetime] = None
    notes: Optional[str] = None


class AssetUpdate(BaseModel):
    name: Optional[str] = None
    current_value: Optional[Decimal] = None
    notes: Optional[str] = None


class AssetResponse(BaseModel):
    id: UUID
    name: str
    asset_type: Optional[str]
    current_value: Decimal
    purchase_value: Optional[Decimal]
    gain: Optional[Decimal] = None
    gain_percent: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Liability Schemas ============

class LiabilityCreate(BaseModel):
    name: str = Field(max_length=100)
    liability_type: str  # home_loan, car_loan, personal_loan, credit_card, emi, bnpl, other
    current_balance: Decimal
    principal_amount: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    emi_amount: Optional[Decimal] = None
    emi_day: Optional[int] = Field(None, ge=1, le=31)
    lender: Optional[str] = None


class LiabilityUpdate(BaseModel):
    current_balance: Optional[Decimal] = None
    emi_amount: Optional[Decimal] = None
    notes: Optional[str] = None


class LiabilityResponse(BaseModel):
    id: UUID
    name: str
    liability_type: Optional[str]
    principal_amount: Optional[Decimal]
    current_balance: Decimal
    interest_rate: Optional[Decimal]
    emi_amount: Optional[Decimal]
    lender: Optional[str]
    paid_percent: Optional[float] = None
    created_at: datetime

    class Config:
        from_attributes = True


class LiabilityListResponse(BaseModel):
    liabilities: List[LiabilityResponse]
    total_liability: Decimal
    monthly_emi_total: Decimal


# ============ Insight Schemas ============

class InsightResponse(BaseModel):
    id: UUID
    insight_type: str
    title: str
    description: str
    severity: str
    priority: int
    data: Optional[dict]
    cta_text: Optional[str]
    cta_link: Optional[str]
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


class InsightListResponse(BaseModel):
    insights: List[InsightResponse]
    unread_count: int


# ============ Portfolio Schemas ============

class PortfolioBreakdown(BaseModel):
    banks: Decimal = Decimal("0")
    investments: Decimal = Decimal("0")
    crypto: Decimal = Decimal("0")
    wallets: Decimal = Decimal("0")
    manual_assets: Decimal = Decimal("0")


class PortfolioResponse(BaseModel):
    net_worth: Decimal
    net_worth_change: Decimal
    net_worth_change_percent: float
    total_assets: Decimal
    total_liabilities: Decimal
    breakdown: PortfolioBreakdown
    connected_accounts: int
    last_updated: datetime


class NetWorthHistoryItem(BaseModel):
    date: datetime
    net_worth: Decimal


class NetWorthHistoryResponse(BaseModel):
    history: List[NetWorthHistoryItem]
    growth: dict


# ============ Billing Schemas ============

class CheckoutRequest(BaseModel):
    plan: str  # pro, business
    billing_cycle: str = "monthly"  # monthly, yearly
    provider: str = "stripe"  # stripe, razorpay


class CheckoutResponse(BaseModel):
    checkout_url: str
    session_id: str


class SubscriptionResponse(BaseModel):
    plan: str
    status: str
    billing_cycle: str
    current_period_end: Optional[datetime]
    max_accounts: int
