from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, Account, AccountType, Subscription
from app.schemas import AccountCreate, AccountUpdate, AccountResponse, AccountListResponse
from app.auth import get_current_user

router = APIRouter()


async def check_account_limit(user: User, db: AsyncSession) -> bool:
    """Check if user has reached their account limit."""
    # Get subscription
    sub_result = await db.execute(
        select(Subscription).where(Subscription.user_id == user.id)
    )
    subscription = sub_result.scalar_one_or_none()
    
    max_accounts = subscription.max_accounts if subscription else 2
    
    # Count existing accounts
    count_result = await db.execute(
        select(func.count(Account.id))
        .where(Account.user_id == user.id)
        .where(Account.is_archived == False)
    )
    current_count = count_result.scalar() or 0
    
    return current_count < max_accounts


@router.get("", response_model=AccountListResponse)
async def list_accounts(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
    include_archived: bool = False
):
    """List all accounts for current user."""
    query = (
        select(Account)
        .where(Account.user_id == current_user.id)
    )
    
    if not include_archived:
        query = query.where(Account.is_archived == False)
    
    query = query.order_by(Account.created_at.desc())
    
    result = await db.execute(query)
    accounts = result.scalars().all()
    
    # Get account type names
    account_responses = []
    by_type = {}
    
    for account in accounts:
        # Get type name
        type_name = None
        if account.account_type_id:
            type_result = await db.execute(
                select(AccountType.name).where(AccountType.id == account.account_type_id)
            )
            type_name = type_result.scalar()
        
        account_resp = AccountResponse(
            id=account.id,
            name=account.name,
            institution=account.institution,
            account_type=type_name,
            current_balance=account.current_balance,
            currency=account.currency,
            connection_type=account.connection_type,
            last_synced_at=account.last_synced_at,
            sync_status=account.sync_status,
            created_at=account.created_at
        )
        account_responses.append(account_resp)
        
        # Count by type
        by_type[type_name or "other"] = by_type.get(type_name or "other", 0) + 1
    
    return AccountListResponse(
        accounts=account_responses,
        total=len(account_responses),
        by_type=by_type
    )


@router.post("", response_model=AccountResponse, status_code=status.HTTP_201_CREATED)
async def create_account(
    account_data: AccountCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new account."""
    # Check limit
    if not await check_account_limit(current_user, db):
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail={
                "code": "ACCOUNT_LIMIT_EXCEEDED",
                "message": "You've reached your account limit. Upgrade to add more accounts.",
                "upgrade_url": "/billing/checkout?plan=pro"
            }
        )
    
    # Get account type ID
    type_result = await db.execute(
        select(AccountType.id).where(AccountType.name == account_data.account_type)
    )
    account_type_id = type_result.scalar()
    
    account = Account(
        user_id=current_user.id,
        account_type_id=account_type_id,
        name=account_data.name,
        institution=account_data.institution,
        current_balance=account_data.current_balance,
        currency=account_data.currency,
        connection_type="manual"
    )
    
    db.add(account)
    await db.commit()
    await db.refresh(account)
    
    return AccountResponse(
        id=account.id,
        name=account.name,
        institution=account.institution,
        account_type=account_data.account_type,
        current_balance=account.current_balance,
        currency=account.currency,
        connection_type=account.connection_type,
        last_synced_at=account.last_synced_at,
        sync_status=account.sync_status,
        created_at=account.created_at
    )


@router.get("/{account_id}", response_model=AccountResponse)
async def get_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get account by ID."""
    result = await db.execute(
        select(Account)
        .where(Account.id == account_id)
        .where(Account.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()
    
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Get type name
    type_name = None
    if account.account_type_id:
        type_result = await db.execute(
            select(AccountType.name).where(AccountType.id == account.account_type_id)
        )
        type_name = type_result.scalar()
    
    return AccountResponse(
        id=account.id,
        name=account.name,
        institution=account.institution,
        account_type=type_name,
        current_balance=account.current_balance,
        currency=account.currency,
        connection_type=account.connection_type,
        last_synced_at=account.last_synced_at,
        sync_status=account.sync_status,
        created_at=account.created_at
    )


@router.patch("/{account_id}", response_model=AccountResponse)
async def update_account(
    account_id: UUID,
    account_data: AccountUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update account."""
    result = await db.execute(
        select(Account)
        .where(Account.id == account_id)
        .where(Account.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()
    
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    if account_data.name is not None:
        account.name = account_data.name
    if account_data.institution is not None:
        account.institution = account_data.institution
    if account_data.current_balance is not None:
        account.current_balance = account_data.current_balance
    if account_data.is_hidden is not None:
        account.is_hidden = account_data.is_hidden
    
    await db.commit()
    await db.refresh(account)
    
    # Get type name
    type_name = None
    if account.account_type_id:
        type_result = await db.execute(
            select(AccountType.name).where(AccountType.id == account.account_type_id)
        )
        type_name = type_result.scalar()
    
    return AccountResponse(
        id=account.id,
        name=account.name,
        institution=account.institution,
        account_type=type_name,
        current_balance=account.current_balance,
        currency=account.currency,
        connection_type=account.connection_type,
        last_synced_at=account.last_synced_at,
        sync_status=account.sync_status,
        created_at=account.created_at
    )


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete account."""
    result = await db.execute(
        select(Account)
        .where(Account.id == account_id)
        .where(Account.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()
    
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    await db.delete(account)
    await db.commit()


@router.post("/{account_id}/sync")
async def sync_account(
    account_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Force sync account (for API-connected accounts)."""
    result = await db.execute(
        select(Account)
        .where(Account.id == account_id)
        .where(Account.user_id == current_user.id)
    )
    account = result.scalar_one_or_none()
    
    if account is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    if account.connection_type == "manual":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Manual accounts cannot be synced"
        )
    
    # TODO: Implement actual sync logic based on provider
    account.last_synced_at = datetime.utcnow()
    account.sync_status = "ok"
    await db.commit()
    
    return {"message": "Account synced successfully", "last_synced_at": account.last_synced_at}
