# Payfolio - Product Requirements Document (PRD)

## 1. Executive Summary
Payfolio is an all-in-one platform for freelancers to showcase their work and get paid. It combines a "Link-in-bio" style portfolio with native invoicing, contract management, and payment processing.

## 2. User Roles
- **Creator (Freelancer):** Sets up portfolio, creates services, sends invoices, manages clients.
- **Client (Guest/User):** Views portfolio, purchases services, pays invoices, signs contracts.
- **System:** Handles payments (Stripe Connect), generates PDFs (Invoices/Contracts).

## 3. Features & Scope
### MVP (Phase 1 - Days 16-30)
- **Portfolio Builder:** Drag-and-drop editor for projects, "About Me", and "Services".
- **Service Listings:** Productized services (e.g., "Logo Design - $500") with checkout.
- **Invoicing:** Create and send invoices via email (Stripe integration).
- **Client CRM:** Simple list of past clients and revenue.
- **Custom Domain:** Subdomain support (payfolio.co/username).

### Phase 2 (Future)
- **Escrow:** Hold funds until milestone approval.
- **Recurring Retainers:** Auto-charge clients monthly.
- **Contract Templates:** Pre-vetted legal templates for freelancers.

## 4. Monetization Strategy
- **Free Plan:** 3% per transaction + Stripe Fees.
- **Pro Plan ($29/mo):** 0% Platform Fee + Custom Domain + Analytics.

## 5. Functional Requirements
- **Auth:** Email/Password + Google (NextAuth).
- **Payments:** Stripe Connect (Express/Standard accounts for payouts).
- **CMS:** Flexible schema for user portfolios (PostgreSQL JSONB).
- **File Storage:** AWS S3 for portfolio images/PDFs.

## 6. Non-Functional Requirements
- **SEO:** Portfolios must be SSR (Server-Side Rendered) for Google indexing.
- **Speed:** Portfolio load time < 1.5s (LCP).
- **Security:** PCI Compliance (handled via Stripe Elements).

## 7. Success Metrics
- **GPV (Gross Payment Volume):** Total $ processed through invoices.
- **Active Portfolios:** Portfolios with at least 1 view per week.
- **Conversion:** Visitor -> Paid Client rate.
