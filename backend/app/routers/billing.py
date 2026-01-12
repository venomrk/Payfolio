from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db
from app.models import User, Subscription
from app.schemas import CheckoutRequest, CheckoutResponse, SubscriptionResponse
from app.auth import get_current_user

router = APIRouter()


@router.get("/subscription", response_model=SubscriptionResponse)
async def get_subscription(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current user subscription status."""
    result = await db.execute(
        select(Subscription).where(Subscription.user_id == current_user.id)
    )
    sub = result.scalar_one_or_none()
    
    if not sub:
        # Create default free subscription
        sub = Subscription(user_id=current_user.id, plan="free", max_accounts=2)
        db.add(sub)
        await db.commit()
        await db.refresh(sub)
        
    return SubscriptionResponse(
        plan=sub.plan,
        status=sub.status,
        billing_cycle=sub.billing_cycle,
        current_period_end=sub.current_period_end,
        max_accounts=sub.max_accounts
    )


@router.post("/checkout", response_model=CheckoutResponse)
async def create_checkout_session(
    checkout_data: CheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a checkout session (stub implementation)."""
    # NOTE: Actual implementation would integrate Stripe/Razorpay SDKs here
    
    if checkout_data.provider not in ["stripe", "razorpay"]:
        raise HTTPException(status_code=400, detail="Invalid provider")
        
    # Mock response for MVP
    mock_url = f"https://checkout.{checkout_data.provider}.com/pay/mock_session_id"
    
    # In a real app, you would:
    # 1. Create Checkout Session with Stripe/Razorpay
    # 2. Return the session ID and redirect URL
    
    return CheckoutResponse(
        checkout_url=mock_url,
        session_id="sess_mock_123456789"
    )

# Webhook endpoint would go here
@router.post("/webhook")
async def payment_webhook():
    return {"status": "received"}
