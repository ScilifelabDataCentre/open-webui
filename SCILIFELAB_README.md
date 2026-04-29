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

| Variant | Tag suffix | Build args |
| --- | --- | --- |
| Main | none | `BUILD_HASH=${{ github.sha }}` |
| CUDA | `-cuda` | `BUILD_HASH=${{ github.sha }}`, `USE_CUDA=true` |
| CUDA 12.6 | `-cuda126` | `BUILD_HASH=${{ github.sha }}`, `USE_CUDA=true`, `USE_CUDA_VER=cu126` |
| Ollama | `-ollama` | `BUILD_HASH=${{ github.sha }}`, `USE_OLLAMA=true` |
| Slim | `-slim` | `BUILD_HASH=${{ github.sha }}`, `USE_SLIM=true` |

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
