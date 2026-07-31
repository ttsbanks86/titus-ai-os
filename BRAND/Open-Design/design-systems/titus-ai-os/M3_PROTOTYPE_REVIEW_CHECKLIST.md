# M3 Prototype Review Checklist

**Date:** 2026-07-31
**Status:** Ready for Titus Review

---

## Before You Review

The Titus AI OS prototype transforms the backend knowledge engine into an understandable, branded interface. It answers these questions:

1. What project am I in?
2. What milestone is running?
3. What has been completed?
4. What is the agent doing now?
5. Is anything blocked?
6. What decision needs my approval?
7. Are tests passing?
8. Is the system secure?
9. What happens next?

---

## Review Checklist

### Brand Compliance
- [ ] Uses approved Navy/Gold/Cream palette
- [ ] Uses Inter typography (body) and display font (headings)
- [ ] Follows 60-30-10 color rule
- [ ] No unauthorized brand deviations
- [ ] Logo usage follows Master Brand Standards

### Usability
- [ ] Can identify current project in < 3 seconds
- [ ] Can identify current milestone in < 3 seconds
- [ ] Can see test status at a glance
- [ ] Can see agent status at a glance
- [ ] Quick actions are clearly labeled
- [ ] Navigation is intuitive

### Accessibility
- [ ] All interactive elements have visible focus
- [ ] Color is not the only signal
- [ ] Touch targets are 44x44px minimum
- [ ] Keyboard navigation works
- [ ] Screen reader labels present

### Technical
- [ ] Responsive at 375px+ width
- [ ] Dark mode supported
- [ ] Loading states defined
- [ ] Error states defined
- [ ] Empty states defined

### Content
- [ ] Clear, direct language
- [ ] No corporate filler
- [ ] No em dashes
- [ ] Status labels are unambiguous

---

## What to Look For

### Good Signs
- You can understand the system state without asking questions
- Status indicators are immediately clear
- Quick actions feel safe and obvious
- The brand feels consistent and professional

### Concerns
- Anything that requires explanation
- Ambiguous status labels
- Missing states (what happens when X fails?)
- Overly technical jargon

---

## Decision Required

After review, please indicate:

- [ ] **Approved** — Proceed to implementation
- [ ] **Approved with changes** — List changes needed
- [ ] **Needs revision** — Major concerns to address

---

## Next Steps After Approval

1. Implement interface following prototype spec
2. Build components with brand tokens
3. Test all states (empty, loading, error, success)
4. Verify accessibility
5. Document implementation
