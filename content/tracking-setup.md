# 📊 Tracking & Pixel Setup: MoonLIT Arc

> **Project:** PRJ-001 (MoonLIT Arc Pipeline)
> **Status:** Draft / Pending Real IDs
> **Objective:** Implement GTM, Google Ads Conversion Tracking, and Meta Pixel.

---

## 1. Google Tag Manager (GTM)
The primary container for all tracking.

### Head Script
```html
<!-- Google Tag Manager -->
<script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':
new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],
j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
})(window,document,'script','dataLayer','GTM-XXXXXXX');</script>
<!-- End Google Tag Manager -->
```

### Body Script
```html
<!-- Google Tag Manager (noscript) -->
<noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-XXXXXXX"
height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
<!-- End Google Tag Manager (noscript) -->
```

---

## 2. Meta Pixel (Facebook Ads)
Track visitors and optimize for lead conversions.

### Implementation Logic
- **Base Code:** Installed via GTM on all pages.
- **Event (Lead):** Triggered on form submission success on the review landing page.

```javascript
fbq('track', 'Lead', {
  content_category: 'Review Engine',
  value: 49.00,
  currency: 'USD'
});
```

---

## 3. Google Ads Conversion Tracking
Specifically for the Search campaigns.

### Conversion Events
1. **Lead Form Submission:** Tracked when a user fills the contact form.
2. **Review Link Click:** Tracked as a micro-conversion.

---

## 4. Integration with The Review Engine
The tracking scripts should be injected into:
- `projects/review-engine/src/frontend/app/layout.tsx` (Global)
- `projects/review-engine/src/frontend/app/review/[id]/page.tsx` (Landing Page)

---

## 5. Next Steps
1. [ ] Sani to provide GTM Container ID (`GTM-XXXXXXX`).
2. [ ] Sani to provide Meta Pixel ID.
3. [ ] Alfred to inject scripts into the Next.js frontend once IDs are confirmed.
