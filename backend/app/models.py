from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from uuid import UUID
import sqlalchemy as sa
from sqlalchemy import String, Boolean, DateTime, Integer, Numeric, Text, ForeignKey, ARRAY
from sqlalchemy.dialects.postgresql import UUID as PGUUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class User(Base):
    __tablename__ = "users"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    password_hash: Mapped[Optional[str]] = mapped_column(String(255))
    full_name: Mapped[Optional[str]] = mapped_column(String(255))
    phone: Mapped[Optional[str]] = mapped_column(String(20))
    avatar_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Subscription
    plan: Mapped[str] = mapped_column(String(20), default="free")
    plan_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    # Preferences
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    locale: Mapped[str] = mapped_column(String(10), default="en-IN")
    theme: Mapped[str] = mapped_column(String(10), default="dark")
    
    # Metadata
    email_verified: Mapped[bool] = mapped_column(Boolean, default=False)
    last_login_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    
    # Relationships
    accounts: Mapped[List["Account"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    assets: Mapped[List["Asset"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    liabilities: Mapped[List["Liability"]] = relationship(back_populates="user", cascade="all, delete-orphan")
    insights: Mapped[List["Insight"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class AccountType(Base):
    __tablename__ = "account_types"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    color: Mapped[Optional[str]] = mapped_column(String(7))
    is_asset: Mapped[bool] = mapped_column(Boolean, default=True)
    
    accounts: Mapped[List["Account"]] = relationship(back_populates="account_type")


class Account(Base):
    __tablename__ = "accounts"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_type_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("account_types.id"))
    
    # Display
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    institution: Mapped[Optional[str]] = mapped_column(String(100))
    logo_url: Mapped[Optional[str]] = mapped_column(Text)
    
    # Balance
    current_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    available_balance: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2))
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    
    # Connection
    connection_type: Mapped[str] = mapped_column(String(20), default="manual")
    provider: Mapped[Optional[str]] = mapped_column(String(50))
    provider_account_id: Mapped[Optional[str]] = mapped_column(String(255))
    access_token_encrypted: Mapped[Optional[str]] = mapped_column(Text)
    
    # Sync
    last_synced_at: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    sync_status: Mapped[str] = mapped_column(String(20), default="ok")
    sync_error: Mapped[Optional[str]] = mapped_column(Text)
    
    # Metadata
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)
    is_archived: Mapped[bool] = mapped_column(Boolean, default=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="accounts")
    account_type: Mapped[Optional["AccountType"]] = relationship(back_populates="accounts")
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="account", cascade="all, delete-orphan")


class Category(Base):
    __tablename__ = "categories"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String(50), nullable=False)
    parent_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"))
    icon: Mapped[Optional[str]] = mapped_column(String(50))
    color: Mapped[Optional[str]] = mapped_column(String(7))
    is_income: Mapped[bool] = mapped_column(Boolean, default=False)
    
    transactions: Mapped[List["Transaction"]] = relationship(back_populates="category")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    account_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("accounts.id", ondelete="CASCADE"), nullable=False)
    category_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("categories.id"))
    
    # Core
    amount: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    transaction_type: Mapped[Optional[str]] = mapped_column(String(20))
    
    # Details
    description: Mapped[Optional[str]] = mapped_column(Text)
    merchant_name: Mapped[Optional[str]] = mapped_column(String(255))
    merchant_logo: Mapped[Optional[str]] = mapped_column(Text)
    
    # Classification
    is_recurring: Mapped[bool] = mapped_column(Boolean, default=False)
    is_subscription: Mapped[bool] = mapped_column(Boolean, default=False)
    tags: Mapped[Optional[List[str]]] = mapped_column(ARRAY(Text))
    
    # Source
    provider_transaction_id: Mapped[Optional[str]] = mapped_column(String(255))
    raw_data: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    # AI
    ai_category_confidence: Mapped[Optional[Decimal]] = mapped_column(Numeric(3, 2))
    ai_insights: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    # Dates
    transaction_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    posted_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    
    # Relationships
    user: Mapped["User"] = relationship(back_populates="transactions")
    account: Mapped["Account"] = relationship(back_populates="transactions")
    category: Mapped[Optional["Category"]] = relationship(back_populates="transactions")


class Asset(Base):
    __tablename__ = "assets"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    asset_type: Mapped[Optional[str]] = mapped_column(String(50))
    
    current_value: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    purchase_value: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2))
    purchase_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    
    user: Mapped["User"] = relationship(back_populates="assets")


class Liability(Base):
    __tablename__ = "liabilities"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    linked_account_id: Mapped[Optional[UUID]] = mapped_column(PGUUID(as_uuid=True), ForeignKey("accounts.id"))
    
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    liability_type: Mapped[Optional[str]] = mapped_column(String(50))
    
    principal_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2))
    current_balance: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    interest_rate: Mapped[Optional[Decimal]] = mapped_column(Numeric(5, 2))
    currency: Mapped[str] = mapped_column(String(3), default="INR")
    
    emi_amount: Mapped[Optional[Decimal]] = mapped_column(Numeric(18, 2))
    emi_day: Mapped[Optional[int]] = mapped_column(Integer)
    start_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    end_date: Mapped[Optional[datetime]] = mapped_column(DateTime)
    
    lender: Mapped[Optional[str]] = mapped_column(String(100))
    notes: Mapped[Optional[str]] = mapped_column(Text)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())
    
    user: Mapped["User"] = relationship(back_populates="liabilities")


class Insight(Base):
    __tablename__ = "insights"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    insight_type: Mapped[str] = mapped_column(String(50), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=False)
    
    severity: Mapped[str] = mapped_column(String(20), default="info")
    priority: Mapped[int] = mapped_column(Integer, default=5)
    
    data: Mapped[Optional[dict]] = mapped_column(JSONB)
    cta_text: Mapped[Optional[str]] = mapped_column(String(100))
    cta_link: Mapped[Optional[str]] = mapped_column(String(255))
    
    is_read: Mapped[bool] = mapped_column(Boolean, default=False)
    is_dismissed: Mapped[bool] = mapped_column(Boolean, default=False)
    
    valid_from: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    valid_until: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    
    user: Mapped["User"] = relationship(back_populates="insights")


class Subscription(Base):
    __tablename__ = "subscriptions"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    plan: Mapped[str] = mapped_column(String(20), default="free", nullable=False)
    status: Mapped[str] = mapped_column(String(20), default="active")
    
    stripe_customer_id: Mapped[Optional[str]] = mapped_column(String(255))
    stripe_subscription_id: Mapped[Optional[str]] = mapped_column(String(255))
    razorpay_customer_id: Mapped[Optional[str]] = mapped_column(String(255))
    razorpay_subscription_id: Mapped[Optional[str]] = mapped_column(String(255))
    
    billing_cycle: Mapped[str] = mapped_column(String(20), default="monthly")
    current_period_start: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    
    max_accounts: Mapped[int] = mapped_column(Integer, default=2)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now(), onupdate=sa.func.now())


class NetWorthHistory(Base):
    __tablename__ = "net_worth_history"
    
    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, server_default=sa.text("gen_random_uuid()"))
    user_id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    
    snapshot_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    
    total_assets: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    total_liabilities: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    net_worth: Mapped[Decimal] = mapped_column(Numeric(18, 2), nullable=False)
    
    breakdown: Mapped[Optional[dict]] = mapped_column(JSONB)
    
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=sa.func.now())
