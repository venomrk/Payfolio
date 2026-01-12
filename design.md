# Payfolio - UI/UX Design System

## 1. Design Philosophy
Modern, minimal, and creator-focused. "Notion-like" simplicity but with financial trust.
- **Aesthetic:** Clean typography, generous whitespace, subtle shadows.
- **Vibe:** "Your personal corner of the internet that prints money."

## 2. Color System
### Primary
- **Midnight Black:** `#000000` (Primary Buttons, Text)
- **Paper White:** `#FFFFFF` (Backgrounds, Cards)
- **Accent Green:** `#22C55E` (Revenue, Success, "Get Paid")
- **Soft Gray:** `#F3F4F6` (Backgrounds, Inputs)

### Functional
- **Border:** `#E5E7EB`
- **Text Secondary:** `#6B7280`
- **Error:** `#EF4444`

## 3. Typography
**Font:** Inter (or Geist Sans if available)
- **H1:** 36px, Bold, Tracking -0.03em
- **H2:** 24px, SemiBold
- **Body:** 16px, Regular, Line-height 1.6
- **Mono:** JetBrains Mono (for Invoice numbers, code snippets)

## 4. Components
### The "Portfolio Block"
A modular component that users stack to build their page.
- **Header:** Avatar + Name + Bio + Social Links.
- **Service Card:** Title + Price + "Buy Now" button.
- **Gallery:** Grid of 3 images.

### The "Invoice"
A clean, paper-like card centered on screen.
- Top: Logo + Bill To.
- Middle: Line items table.
- Bottom: "Pay with Stick" (Apple Pay / Card) button.

## 5. User Flows
### Flow A: Onboarding (The "Magic" Moment)
1.  **Landing:** "Claim your payfolio.co/username" input.
2.  **Signup:** Email/Password.
3.  **Setup:** Upload Avatar -> Add Stripe Connect -> Ready.
4.  **Result:** User lands on their live public page instantly.

### Flow B: Send an Invoice
1.  **Dashboard:** Click "New Invoice" (+).
2.  **Form:** Client Email, Amount, Description.
3.  **Send:** System generates a unique link (payfolio.co/i/xj92s).
4.  **Track:** Status changes from "Sent" -> "Viewed" -> "Paid".

## 6. Dashboards
### Creator Dashboard
- **Overview:** Revenue Graph (Line chart), Recent Invoices list.
- **Edit Page:** Live preview on right, sidebar controls on left.
- **Settings:** Custom Domain, Stripe Payouts.
