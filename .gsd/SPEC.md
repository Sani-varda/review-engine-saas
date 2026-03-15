# SPEC.md — Project Specification

> **Status**: `FINALIZED`
>
> ⚠️ **Planning Lock**: No code may be written until this spec is marked `FINALIZED`.

## Vision
**The Review Engine** is a high-performance, production-ready vertical SaaS designed to help local businesses (Dental Clinics, MedSpas, Salons, etc.) dominate their local market by automating review collection, intelligently gating feedback, and leveraging AI for review management.

## Goals
1. **Automated Review Gating** — Filter customer sentiment before it hits public platforms (4-5 stars to Google, 1-3 stars to private feedback).
2. **AI-Powered Review Management** — Use Gemini-3-Flash to generate personalized, empathetic replies to Google reviews.
3. **Omnichannel Outreach** — Support for SMS (Twilio) and Email (Resend) review requests.
4. **Multi-Platform Support** — Web Dashboard (Next.js) and Mobile App (Flutter).
5. **Real-time Insights** — Analytics for ratings, growth, and conversion.

## Non-Goals (Out of Scope)
- Social media management (Facebook posts, Instagram ads).
- Reputation management for enterprise-level brands (multi-national).
- Full CRM features (invoicing, scheduling - unless integrated as an extension).

## Constraints
- **Technical**: Must be modular (Backend, Frontend, Mobile).
- **Architecture**: Docker-based deployment for portability.
- **Provider**: Agnostic implementation of external APIs (Twilio, Resend, Google).

## Success Criteria
- [x] Functional Backend with FastAPI.
- [x] Interactive Web Dashboard with Next.js.
- [x] Cross-platform Mobile App with Flutter.
- [x] Successful integration with Google Business Profile API.
- [x] Functional AI auto-reply engine.

---

*Last updated: 2026-03-15*
