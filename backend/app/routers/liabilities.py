from typing import List
from uuid import UUID
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, Liability
from app.schemas import LiabilityCreate, LiabilityUpdate, LiabilityResponse, LiabilityListResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=LiabilityListResponse)
async def list_liabilities(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all liabilities."""
    result = await db.execute(
        select(Liability)
        .where(Liability.user_id == current_user.id)
        .order_by(Liability.created_at.desc())
    )
    liabilities = result.scalars().all()
    
    total_liability = Decimal(0)
    monthly_emi_total = Decimal(0)
    
    liability_responses = []
    for l in liabilities:
        resp = LiabilityResponse.model_validate(l)
        if l.principal_amount and l.principal_amount > 0:
            paid_amount = l.principal_amount - l.current_balance
            resp.paid_percent = float((paid_amount / l.principal_amount) * 100)
        else:
            resp.paid_percent = 0.0
            
        liability_responses.append(resp)
        total_liability += l.current_balance
        if l.emi_amount:
            monthly_emi_total += l.emi_amount
            
    return LiabilityListResponse(
        liabilities=liability_responses,
        total_liability=total_liability,
        monthly_emi_total=monthly_emi_total
    )


@router.post("", response_model=LiabilityResponse, status_code=status.HTTP_201_CREATED)
async def create_liability(
    liab_data: LiabilityCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new liability."""
    liability = Liability(
        user_id=current_user.id,
        name=liab_data.name,
        liability_type=liab_data.liability_type,
        current_balance=liab_data.current_balance,
        principal_amount=liab_data.principal_amount,
        interest_rate=liab_data.interest_rate,
        emi_amount=liab_data.emi_amount,
        emi_day=liab_data.emi_day,
        lender=liab_data.lender
    )
    
    db.add(liability)
    await db.commit()
    await db.refresh(liability)
    
    resp = LiabilityResponse.model_validate(liability)
    if liability.principal_amount and liability.principal_amount > 0:
        paid_amount = liability.principal_amount - liability.current_balance
        resp.paid_percent = float((paid_amount / liability.principal_amount) * 100)
        
    return resp


@router.get("/{liab_id}", response_model=LiabilityResponse)
async def get_liability(
    liab_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get liability details."""
    result = await db.execute(
        select(Liability)
        .where(Liability.id == liab_id)
        .where(Liability.user_id == current_user.id)
    )
    liability = result.scalar_one_or_none()
    
    if not liability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liability not found")
        
    resp = LiabilityResponse.model_validate(liability)
    if liability.principal_amount and liability.principal_amount > 0:
        paid_amount = liability.principal_amount - liability.current_balance
        resp.paid_percent = float((paid_amount / liability.principal_amount) * 100)
        
    return resp


@router.patch("/{liab_id}", response_model=LiabilityResponse)
async def update_liability(
    liab_id: UUID,
    liab_data: LiabilityUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update liability."""
    result = await db.execute(
        select(Liability)
        .where(Liability.id == liab_id)
        .where(Liability.user_id == current_user.id)
    )
    liability = result.scalar_one_or_none()
    
    if not liability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liability not found")
        
    if liab_data.current_balance is not None:
        liability.current_balance = liab_data.current_balance
    if liab_data.emi_amount is not None:
        liability.emi_amount = liab_data.emi_amount
    if liab_data.notes is not None:
        liability.notes = liab_data.notes
        
    await db.commit()
    await db.refresh(liability)
    
    resp = LiabilityResponse.model_validate(liability)
    if liability.principal_amount and liability.principal_amount > 0:
        paid_amount = liability.principal_amount - liability.current_balance
        resp.paid_percent = float((paid_amount / liability.principal_amount) * 100)
        
    return resp


@router.delete("/{liab_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_liability(
    liab_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete liability."""
    result = await db.execute(
        select(Liability)
        .where(Liability.id == liab_id)
        .where(Liability.user_id == current_user.id)
    )
    liability = result.scalar_one_or_none()
    
    if not liability:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Liability not found")
        
    await db.delete(liability)
    await db.commit()
