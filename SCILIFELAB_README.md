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
- Signing out uses the backend-provided redirect when available; otherwise it returns the user to `/about`.

How to manage it:

- Update modal text in `src/lib/components/layout/TermsAcceptanceOverlay.svelte`.
- Force re-acceptance by changing `TERMS_AND_CONDITIONS_VERSION` in `src/routes/(app)/+layout.svelte`.
- Disable it by removing the `showTermsAcceptance` gate in `src/routes/(app)/+layout.svelte`.

Current limitation:

- This is frontend enforcement, not backend authorization.

## Public Landing Page

Unauthenticated visitors to protected Open WebUI routes are sent to `/about`.
The landing page is served by a separate Kubernetes deployment in the same
namespace; it is not part of this Open WebUI frontend.

Implementation:

- `gotoAbout` in `src/routes/(app)/+layout.svelte` performs the redirect.
- The local `/welcome` route has been removed.

How it works:

- The authenticated app layout redirects whenever the user store is empty,
  both at initial load and after a user signs out or their session expires.
- The redirect uses `window.location.assign('/about')` rather than Svelte
  navigation, so the browser makes a new request and the ingress can route it
  to the dedicated `/about` deployment.
- Deep links to protected routes also go to `/about`; Open WebUI no longer
  preserves a `redirect` query parameter for unauthenticated users.
- `/auth` remains the Open WebUI login endpoint. After a successful login, its
  existing default redirect returns the user to `/` unless another redirect is
  explicitly supplied.

Deployment requirements:

- Configure the cluster ingress to route `/about` to the public landing-page
  deployment while keeping it on the same public origin as Open WebUI.
- The public landing page should link users to `/auth` when they need to sign in.

## Docker Image Builds

Docker images are built by `.github/workflows/docker-build.yaml`. For
SciLifeLab, the main branch is `scilifelab/main`, and the image build is
normally started by manually running the GitHub Actions workflow from the
Actions tab with `scilifelab/main` selected as the workflow ref.

When it runs:

- For SciLifeLab: manually through `workflow_dispatch` on `scilifelab/main`.
- On pushes to `main` and `dev`.
- On version tags matching `v*`.

Where images are published:

- Primary registry: GitHub Container Registry, `ghcr.io/<owner>/<repo>`.
- The repository and image name are lowercased before publishing.
- On `main` and version tags, images are also copied best-effort to Docker Hub as
  `openwebui/open-webui`. Docker Hub copy failures do not fail the GHCR build.

Image variants:

| Variant   | Tag suffix | Build args                                                            |
| --------- | ---------- | --------------------------------------------------------------------- |
| Main      | none       | `BUILD_HASH=${{ github.sha }}`                                        |
| CUDA      | `-cuda`    | `BUILD_HASH=${{ github.sha }}`, `USE_CUDA=true`                       |
| CUDA 12.6 | `-cuda126` | `BUILD_HASH=${{ github.sha }}`, `USE_CUDA=true`, `USE_CUDA_VER=cu126` |
| Ollama    | `-ollama`  | `BUILD_HASH=${{ github.sha }}`, `USE_OLLAMA=true`                     |
| Slim      | `-slim`    | `BUILD_HASH=${{ github.sha }}`, `USE_SLIM=true`                       |

Each variant is built for both `linux/amd64` and `linux/arm64` using Docker
Buildx. The per-platform jobs push images by digest, upload those digests as
temporary workflow artifacts, and the matching merge job creates and pushes a
multi-platform manifest list for the final tags.

Tagging:

- Branch pushes publish branch tags such as `main`, `dev`, `main-cuda`, or
  `dev-slim`.
- Every build also publishes a Git SHA tag with the `git-` prefix, with the
  variant suffix applied where relevant.
- Version tags such as `v1.2.3` publish semver tags such as `1.2.3` and `1.2`,
  again with the variant suffix applied where relevant.
- Pushes to `main` also publish `latest` for the main image and
  `latest-cuda`, `latest-cuda126`, `latest-ollama`, and `latest-slim` for the
  variants. The CUDA, CUDA 12.6, Ollama, and Slim variants also get short GHCR
  tags `cuda`, `cuda126`, `ollama`, and `slim` on `main`.

Caching:

- Each variant uses a registry-backed Buildx cache in GHCR.
- Cache tags are variant- and platform-specific, for example
  `cache-linux-amd64-main`, `cache-cuda-linux-arm64-main`, or
  `cache-slim-linux-amd64-dev`.
- Tag builds reuse the `main` cache for the matching variant and platform.

Docker Hub copy:

- Runs only for `main` and `v*` tags, after all GHCR manifest lists are created.
- `main` copies `latest`, plus variant tags like `latest-cuda` and `cuda`.
- Version tags copy the version and major/minor tags, for example `1.2.3-cuda`
  and `1.2-cuda`.
