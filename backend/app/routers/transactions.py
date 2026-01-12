from typing import List, Optional
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy import select, func, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database import get_db
from app.models import User, Transaction, Account, Category
from app.schemas import (
    TransactionCreate, 
    TransactionUpdate, 
    TransactionResponse, 
    TransactionListResponse,
    TransactionStats
)
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=TransactionListResponse)
async def list_transactions(
    account_id: Optional[UUID] = None,
    category_id: Optional[int] = None,
    transaction_type: Optional[str] = None,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List transactions with filtering."""
    query = (
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.user_id == current_user.id)
    )
    
    if account_id:
        query = query.where(Transaction.account_id == account_id)
    
    if category_id:
        query = query.where(Transaction.category_id == category_id)
        
    if transaction_type:
        query = query.where(Transaction.transaction_type == transaction_type)
        
    if date_from:
        query = query.where(Transaction.transaction_date >= date_from)
        
    if date_to:
        query = query.where(Transaction.transaction_date <= date_to)
        
    # Get total count
    count_query = select(func.count()).select_from(query.subquery())
    count_result = await db.execute(count_query)
    total = count_result.scalar_one()
    
    # Sort and paginate
    query = query.order_by(desc(Transaction.transaction_date), desc(Transaction.created_at))
    query = query.limit(limit).offset(offset)
    
    result = await db.execute(query)
    transactions = result.scalars().all()
    
    transaction_responses = []
    for txn in transactions:
        # Get account name
        account_name = None
        # Optimization: could join Accounts table or cache this
        if txn.account_id:
            account_res = await db.execute(select(Account.name).where(Account.id == txn.account_id))
            account_name = account_res.scalar_one_or_none()

        response = TransactionResponse.model_validate(txn)
        response.account_name = account_name
        transaction_responses.append(response)

    return TransactionListResponse(
        transactions=transaction_responses,
        total=total,
        limit=limit,
        offset=offset
    )


@router.post("", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
async def create_transaction(
    txn_data: TransactionCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new transaction manually."""
    # Verify account belongs to user
    account_result = await db.execute(
        select(Account).where(Account.id == txn_data.account_id).where(Account.user_id == current_user.id)
    )
    account = account_result.scalar_one_or_none()
    
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    # Create transaction
    txn = Transaction(
        user_id=current_user.id,
        account_id=txn_data.account_id,
        amount=txn_data.amount,
        transaction_type=txn_data.transaction_type,
        description=txn_data.description,
        merchant_name=txn_data.merchant_name,
        category_id=txn_data.category_id,
        transaction_date=txn_data.transaction_date
    )
    
    # Update account balance
    if txn_data.transaction_type == "credit":
        account.current_balance += txn_data.amount
    elif txn_data.transaction_type == "debit":
        account.current_balance -= abs(txn_data.amount)  # Ensure amount is subtracted
        
    db.add(txn)
    await db.commit()
    await db.refresh(txn)

    # Re-fetch with relationships loaded
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.id == txn.id)
    )
    txn = result.scalar_one()

    response = TransactionResponse.model_validate(txn)
    response.account_name = account.name
    return response


@router.get("/{txn_id}", response_model=TransactionResponse)
async def get_transaction(
    txn_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get transaction details."""
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.id == txn_id)
        .where(Transaction.user_id == current_user.id)
    )
    txn = result.scalar_one_or_none()
    
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        
    account_res = await db.execute(select(Account.name).where(Account.id == txn.account_id))
    account_name = account_res.scalar_one_or_none()
    
    response = TransactionResponse.model_validate(txn)
    response.account_name = account_name
    return response


@router.patch("/{txn_id}", response_model=TransactionResponse)
async def update_transaction(
    txn_id: UUID,
    txn_data: TransactionUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update transaction details."""
    result = await db.execute(
        select(Transaction)
        .options(selectinload(Transaction.category))
        .where(Transaction.id == txn_id)
        .where(Transaction.user_id == current_user.id)
    )
    txn = result.scalar_one_or_none()
    
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
    
    if txn_data.description is not None:
        txn.description = txn_data.description
    if txn_data.merchant_name is not None:
        txn.merchant_name = txn_data.merchant_name
    if txn_data.category_id is not None:
        txn.category_id = txn_data.category_id
    if txn_data.tags is not None:
        txn.tags = txn_data.tags
        
    await db.commit()
    await db.refresh(txn)
    
    account_res = await db.execute(select(Account.name).where(Account.id == txn.account_id))
    account_name = account_res.scalar_one_or_none()
    
    response = TransactionResponse.model_validate(txn)
    response.account_name = account_name
    return response


@router.delete("/{txn_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_transaction(
    txn_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete a transaction and revert balance change."""
    result = await db.execute(
        select(Transaction)
        .where(Transaction.id == txn_id)
        .where(Transaction.user_id == current_user.id)
    )
    txn = result.scalar_one_or_none()
    
    if not txn:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Transaction not found")
        
    # Revert account balance
    account_result = await db.execute(
        select(Account).where(Account.id == txn.account_id)
    )
    account = account_result.scalar_one_or_none()
    
    if account:
        if txn.transaction_type == "credit":
            account.current_balance -= txn.amount
        elif txn.transaction_type == "debit":
            account.current_balance += abs(txn.amount)

    await db.delete(txn)
    await db.commit()


@router.get("/stats/summary", response_model=TransactionStats)
async def get_transaction_stats(
    date_from: datetime,
    date_to: datetime,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get summarized transaction statistics."""
    # Income
    income_query = select(func.sum(Transaction.amount)).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date <= date_to,
        Transaction.transaction_type == "credit"
    )
    income = (await db.execute(income_query)).scalar() or Decimal(0)
    
    # Expenses
    expense_query = select(func.sum(Transaction.amount)).where(
        Transaction.user_id == current_user.id,
        Transaction.transaction_date >= date_from,
        Transaction.transaction_date <= date_to,
        Transaction.transaction_type == "debit"
    )
    expenses = (await db.execute(expense_query)).scalar() or Decimal(0)
    
    # Absolute value of expenses for display
    expenses_abs = abs(expenses)
    
    # By category
    cat_query = (
        select(Category.name, func.sum(Transaction.amount).label("total"))
        .join(Transaction, Transaction.category_id == Category.id)
        .where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date <= date_to
        )
        .group_by(Category.name)
    )
    cat_results = (await db.execute(cat_query)).all()
    by_category = [{"category": r.name, "amount": abs(r.total), "percent": 0.0} for r in cat_results]
    
    # Top Merchants
    merch_query = (
        select(Transaction.merchant_name, func.sum(Transaction.amount).label("total"), func.count(Transaction.id).label("count"))
        .where(
            Transaction.user_id == current_user.id,
            Transaction.transaction_date >= date_from,
            Transaction.transaction_date <= date_to,
            Transaction.transaction_type == "debit"
        )
        .group_by(Transaction.merchant_name)
        .order_by(func.sum(Transaction.amount)) # Most negative amount first (largest expense)
        .limit(5)
    )
    merch_results = (await db.execute(merch_query)).all()
    top_merchants = [{"name": r.merchant_name or "Unknown", "amount": abs(r.total), "count": r.count} for r in merch_results]

    return TransactionStats(
        total_income=income,
        total_expenses=expenses_abs,
        net_cash_flow=income - expenses_abs,
        by_category=by_category,
        top_merchants=top_merchants
    )
