from typing import List
from uuid import UUID
from datetime import datetime
from decimal import Decimal

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, Asset
from app.schemas import AssetCreate, AssetUpdate, AssetResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("", response_model=List[AssetResponse])
async def list_assets(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all manual assets."""
    result = await db.execute(
        select(Asset)
        .where(Asset.user_id == current_user.id)
        .order_by(Asset.created_at.desc())
    )
    assets = result.scalars().all()
    
    responses = []
    for asset in assets:
        resp = AssetResponse.model_validate(asset)
        if asset.purchase_value:
            resp.gain = asset.current_value - asset.purchase_value
            if asset.purchase_value > 0:
                resp.gain_percent = float((resp.gain / asset.purchase_value) * 100)
            else:
                resp.gain_percent = 0.0
        responses.append(resp)
        
    return responses


@router.post("", response_model=AssetResponse, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_data: AssetCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new manual asset."""
    asset = Asset(
        user_id=current_user.id,
        name=asset_data.name,
        asset_type=asset_data.asset_type,
        current_value=asset_data.current_value,
        purchase_value=asset_data.purchase_value,
        purchase_date=asset_data.purchase_date,
        notes=asset_data.notes
    )
    
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    
    resp = AssetResponse.model_validate(asset)
    if asset.purchase_value:
        resp.gain = asset.current_value - asset.purchase_value
        if asset.purchase_value > 0:
            resp.gain_percent = float((resp.gain / asset.purchase_value) * 100)
    return resp


@router.get("/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get asset details."""
    result = await db.execute(
        select(Asset)
        .where(Asset.id == asset_id)
        .where(Asset.user_id == current_user.id)
    )
    asset = result.scalar_one_or_none()
    
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        
    resp = AssetResponse.model_validate(asset)
    if asset.purchase_value:
        resp.gain = asset.current_value - asset.purchase_value
        if asset.purchase_value > 0:
            resp.gain_percent = float((resp.gain / asset.purchase_value) * 100)
    return resp


@router.patch("/{asset_id}", response_model=AssetResponse)
async def update_asset(
    asset_id: UUID,
    asset_data: AssetUpdate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update asset."""
    result = await db.execute(
        select(Asset)
        .where(Asset.id == asset_id)
        .where(Asset.user_id == current_user.id)
    )
    asset = result.scalar_one_or_none()
    
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        
    if asset_data.name is not None:
        asset.name = asset_data.name
    if asset_data.current_value is not None:
        asset.current_value = asset_data.current_value
    if asset_data.notes is not None:
        asset.notes = asset_data.notes
        
    await db.commit()
    await db.refresh(asset)
    
    resp = AssetResponse.model_validate(asset)
    if asset.purchase_value:
        resp.gain = asset.current_value - asset.purchase_value
        if asset.purchase_value > 0:
            resp.gain_percent = float((resp.gain / asset.purchase_value) * 100)
    return resp


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Delete asset."""
    result = await db.execute(
        select(Asset)
        .where(Asset.id == asset_id)
        .where(Asset.user_id == current_user.id)
    )
    asset = result.scalar_one_or_none()
    
    if not asset:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Asset not found")
        
    await db.delete(asset)
    await db.commit()
