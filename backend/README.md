# Payfolio Backend

FastAPI backend for Payfolio financial operating system.

## Tech Stack
- Python 3.11+
- FastAPI
- SQLAlchemy + Supabase
- Pydantic v2
- Stripe + Razorpay

## Setup
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## Environment Variables
Create `.env` file:
```
DATABASE_URL=postgresql://user:pass@host:5432/payfolio
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=xxx
JWT_SECRET=your-secret-key
STRIPE_SECRET_KEY=sk_xxx
RAZORPAY_KEY_ID=xxx
RAZORPAY_KEY_SECRET=xxx
GEMINI_API_KEY=xxx
```
