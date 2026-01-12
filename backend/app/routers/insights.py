from typing import List, Optional
from uuid import UUID
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
import google.generativeai as genai

from app.config import get_settings
from app.database import get_db
from app.models import User, Insight, Transaction, Account
from app.schemas import InsightResponse, InsightListResponse
from app.auth import get_current_user

router = APIRouter()
settings = get_settings()

if settings.GEMINI_API_KEY:
    genai.configure(api_key=settings.GEMINI_API_KEY)


@router.get("", response_model=InsightListResponse)
async def list_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get all valid insights for the user."""
    # Get active insights
    query = (
        select(Insight)
        .where(Insight.user_id == current_user.id)
        .where(Insight.is_dismissed == False)
        # .where(Insight.valid_until >= datetime.utcnow()) # Optional: filter expired
        .order_by(Insight.priority.desc(), Insight.created_at.desc())
    )
    
    result = await db.execute(query)
    insights = result.scalars().all()
    
    # Count unread
    unread_count = sum(1 for i in insights if not i.is_read)
    
    return InsightListResponse(
        insights=[InsightResponse.model_validate(i) for i in insights],
        unread_count=unread_count
    )


@router.post("/{insight_id}/read")
async def mark_read(
    insight_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Mark insight as read."""
    result = await db.execute(
        select(Insight)
        .where(Insight.id == insight_id)
        .where(Insight.user_id == current_user.id)
    )
    insight = result.scalar_one_or_none()
    
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
        
    insight.is_read = True
    await db.commit()
    return {"status": "success"}


@router.post("/{insight_id}/dismiss")
async def dismiss_insight(
    insight_id: UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Dismiss insight."""
    result = await db.execute(
        select(Insight)
        .where(Insight.id == insight_id)
        .where(Insight.user_id == current_user.id)
    )
    insight = result.scalar_one_or_none()
    
    if not insight:
        raise HTTPException(status_code=404, detail="Insight not found")
        
    insight.is_dismissed = True
    await db.commit()
    return {"status": "success"}


@router.post("/generate")
async def generate_insights(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Manually trigger AI insight generation."""
    if not settings.GEMINI_API_KEY:
        raise HTTPException(status_code=503, detail="AI service not configured")
        
    # 1. Gather recent data
    transactions_res = await db.execute(
        select(Transaction)
        .where(Transaction.user_id == current_user.id)
        .order_by(Transaction.transaction_date.desc())
        .limit(20)
    )
    transactions = transactions_res.scalars().all()
    
    accounts_res = await db.execute(
        select(Account).where(Account.user_id == current_user.id)
    )
    accounts = accounts_res.scalars().all()
    
    if not transactions and not accounts:
        return {"message": "Not enough data to generate insights"}

    # 2. Construct Prompt
    data_summary = f"User has {len(accounts)} accounts. "
    data_summary += "Recent transactions:\n"
    for txn in transactions:
        data_summary += f"- {txn.transaction_date}: {txn.merchant_name} ({txn.amount} {txn.currency})\n"
        
    prompt = f"""
    Analyze the following financial data for a user and generate 1 or 2 distinct, actionable insights. I need JSON output.
    
    Data:
    {data_summary}
    
    Output format list of objects:
    [
      {{
        "type": "spending_alert",
        "title": "High spending at Merchant",
        "description": "You spent X amount at Merchant this week, which is Y% higher than usual.",
        "severity": "warning",
        "priority": 7
      }}
    ]
    """
    
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = await model.generate_content_async(prompt)
        # cleanup response text if it has markdown ticks
        text = response.text.replace("```json", "").replace("```", "").strip()
        
        import json
        insights_data = json.loads(text)
        
        generated_count = 0
        for item in insights_data:
            insight = Insight(
                user_id=current_user.id,
                insight_type=item.get("type", "general"),
                title=item.get("title", "Financial Insight"),
                description=item.get("description", ""),
                severity=item.get("severity", "info"),
                priority=item.get("priority", 5),
                is_read=False,
                is_dismissed=False
            )
            db.add(insight)
            generated_count += 1
            
        await db.commit()
        return {"message": f"Generated {generated_count} insights"}
        
    except Exception as e:
        print(f"AI Generation Error: {e}")
        return {"message": "Failed to generate insights", "error": str(e)}
