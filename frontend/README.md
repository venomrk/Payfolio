# Payfolio Frontend

Next.js 14 frontend for Payfolio financial dashboard.

## Tech Stack
- Next.js 14 (App Router)
- TypeScript
- TailwindCSS
- Recharts (charts)
- Lucide React (icons)

## Setup

```bash
cd frontend
npm install
npm run dev
```

## Environment Variables

Create `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure

```
src/
├── app/
│   ├── page.tsx          # Landing page
│   ├── login/page.tsx    # Login
│   ├── signup/page.tsx   # Signup
│   └── dashboard/
│       └── page.tsx      # Main dashboard
├── components/           # Reusable components
└── lib/
    ├── api.ts           # API client
    └── utils.ts         # Helper functions
```

## Features
- Premium dark mode design
- Net worth tracking
- Account aggregation
- AI-powered insights
- Responsive layout
