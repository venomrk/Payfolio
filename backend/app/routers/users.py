from decimal import Decimal
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, Account, AccountType, Asset, Liability, NetWorthHistory
from app.schemas import UserResponse, PortfolioResponse, PortfolioBreakdown
from app.auth import get_current_user

router = APIRouter()


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)


@router.patch("/me", response_model=UserResponse)
async def update_profile(
    full_name: str = None,
    currency: str = None,
    theme: str = None,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update current user profile."""
    if full_name is not None:
        current_user.full_name = full_name
    if currency is not None:
        current_user.currency = currency
    if theme is not None:
        current_user.theme = theme
    
    await db.commit()
    await db.refresh(current_user)
    
    return UserResponse.model_validate(current_user)


@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete current user account and all associated data."""
    await db.delete(current_user)
    await db.commit()


@router.get("/me/portfolio", response_model=PortfolioResponse)
async def get_portfolio(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get portfolio summary for current user."""
    
    # Calculate totals from accounts
    result = await db.execute(
        select(
            func.coalesce(func.sum(
                func.case((AccountType.is_asset == True, Account.current_balance), else_=Decimal(0))
            ), Decimal(0)).label("total_account_assets"),
            func.count(Account.id).label("account_count")
        )
        .select_from(Account)
        .outerjoin(AccountType, Account.account_type_id == AccountType.id)
        .where(Account.user_id == current_user.id)
        .where(Account.is_archived == False)
    )
    row = result.one()
    total_account_assets = row.total_account_assets or Decimal(0)
    account_count = row.account_count or 0
    
    # Get breakdown by type
    breakdown_result = await db.execute(
        select(
            AccountType.name,
            func.coalesce(func.sum(Account.current_balance), Decimal(0)).label("total")
        )
        .select_from(Account)
        .outerjoin(AccountType, Account.account_type_id == AccountType.id)
        .where(Account.user_id == current_user.id)
        .where(Account.is_archived == False)
        .group_by(AccountType.name)
    )
    breakdown_rows = breakdown_result.all()
    
    breakdown = PortfolioBreakdown()
    for row in breakdown_rows:
        if row.name == "bank":
            breakdown.banks = row.total
        elif row.name == "investment":
            breakdown.investments = row.total
        elif row.name == "crypto":
            breakdown.crypto = row.total
        elif row.name == "wallet":
            breakdown.wallets = row.total
    
    # Manual assets
    assets_result = await db.execute(
        select(func.coalesce(func.sum(Asset.current_value), Decimal(0)))
        .where(Asset.user_id == current_user.id)
    )
    manual_assets = assets_result.scalar() or Decimal(0)
    breakdown.manual_assets = manual_assets
    
    # Liabilities
    liabilities_result = await db.execute(
        select(func.coalesce(func.sum(Liability.current_balance), Decimal(0)))
        .where(Liability.user_id == current_user.id)
    )
    total_liabilities = liabilities_result.scalar() or Decimal(0)
    
    # Calculate net worth
    total_assets = total_account_assets + manual_assets
    net_worth = total_assets - total_liabilities
    
    # Get previous month's net worth for comparison
    last_month_result = await db.execute(
        select(NetWorthHistory.net_worth)
        .where(NetWorthHistory.user_id == current_user.id)
        .order_by(NetWorthHistory.snapshot_date.desc())
        .limit(1)
    )
    last_net_worth = last_month_result.scalar() or net_worth
    
    net_worth_change = net_worth - last_net_worth
    change_percent = float((net_worth_change / last_net_worth * 100)) if last_net_worth != 0 else 0
    
    return PortfolioResponse(
        net_worth=net_worth,
        net_worth_change=net_worth_change,
        net_worth_change_percent=round(change_percent, 2),
        total_assets=total_assets,
        total_liabilities=total_liabilities,
        breakdown=breakdown,
        connected_accounts=account_count,
        last_updated=datetime.utcnow()
    )
