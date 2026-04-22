# SciLifeLab README

## Terms and Conditions Modal

This repo includes a SciLifeLab-specific first-login terms modal.

Implementation:

- `src/routes/(app)/+layout.svelte`
- `src/lib/components/layout/TermsAcceptanceOverlay.svelte`

How it works:

- After sign-in, the app checks `user.settings.ui.termsAcceptedVersion`.
- If it does not match the current frontend version, the modal blocks the app.
- Accepting stores `termsAcceptedAt` and `termsAcceptedVersion` in user settings.
- Signing out returns the user to `/auth`.

How to manage it:

- Update modal text in `src/lib/components/layout/TermsAcceptanceOverlay.svelte`.
- Force re-acceptance by changing `TERMS_AND_CONDITIONS_VERSION` in `src/routes/(app)/+layout.svelte`.
- Disable it by removing the `showTermsAcceptance` gate in `src/routes/(app)/+layout.svelte`.

Current limitation:

- This is frontend enforcement, not backend authorization.
