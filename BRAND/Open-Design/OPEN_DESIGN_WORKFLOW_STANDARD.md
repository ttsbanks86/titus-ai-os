# Open Design Workflow Standard

**Date:** 2026-07-31
**Status:** Established

---

## Standard Workflow

Every Titus application follows this Open Design workflow:

### Step 1: Read Approved Brand System
- Read `BRAND/Brand-System/Master-Brand-Standards.md`
- Read `BRAND/tokens.json` and `BRAND/tokens.css`
- Read `BRAND/DESIGN.md`
- Confirm color, typography, spacing, and component tokens

### Step 2: Read Project Source of Truth
- Read the project's authoritative documentation
- Confirm objectives, constraints, and success criteria
- Identify the target audience and use cases

### Step 3: Audit Existing Reusable Components
- Check `BRAND/Open-Design/design-systems/` for existing packages
- Check `BRAND/Asset-Library/` for existing assets
- Identify what can be reused vs. what must be created

### Step 4: Generate Open Design Prototype
- Create structured prototype specification
- Define views, components, states, interactions
- Apply brand tokens consistently
- Include accessibility requirements

### Step 5: Store Prototype Evidence
- Save prototype spec to project directory
- Record design decisions and rationale
- Document any brand deviations with justification

### Step 6: Obtain Owner Approval
- Present prototype to Titus for review
- Record approval or revision requests
- Do not proceed to implementation without approval

### Step 7: Implement from Approved Prototype
- Build interface following prototype spec
- Use brand tokens, not hardcoded values
- Implement all states (empty, loading, error, success)

### Step 8: Verify Implementation
- Compare implementation against prototype
- Check brand compliance
- Test accessibility
- Document any deviations

---

## Prototype Storage

All prototypes are stored in:
```
BRAND/Open-Design/design-systems/[project-name]/
```

Each prototype includes:
- `DESIGN.md` — Full design specification
- `open-design.json` — Plugin manifest
- `README.md` — Usage instructions

---

## Approval Gates

The following require explicit Titus approval:
- New brand colors or typography
- Major layout changes
- New component patterns
- Dark mode implementation
- Mobile-first redesigns

The following do not require approval:
- Using existing brand tokens
- Implementing approved prototypes
- Bug fixes and polish
- Accessibility improvements
- Performance optimizations
