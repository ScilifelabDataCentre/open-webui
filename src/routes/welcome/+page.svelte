<script lang="ts">
	import { onMount } from 'svelte';
	import { user } from '$lib/stores';

	// SciLifeLab-specific public landing page, shown to visitors who are not signed in.
	// Content mirrors https://open-llm.scilifelab.se/guides/ and the use policy.
	const GUIDES_URL = 'https://open-llm.scilifelab.se/guides';
	const USE_POLICY_URL = 'https://open-llm.scilifelab.se/use-policy/';
	const CONTACT_EMAIL = 'open-llm@scilifelab.se';

	let origin = 'https://open-llm.scilifelab.se';

	$: signedIn = !!$user;
	$: primaryHref = signedIn ? '/' : '/auth';
	$: primaryLabel = signedIn ? 'Open the chat' : 'Log in to Open LLM';

	const guides = [
		{
			href: `${GUIDES_URL}/getting-started-api/`,
			title: 'Getting started with the API',
			text: 'Set up your API key and make your first request with curl or Python.'
		},
		{
			href: `${GUIDES_URL}/using-api-coding-agents/`,
			title: 'Using the API with QwenCode',
			text: 'Run an open-source coding agent against models hosted in Sweden.'
		},
		{
			href: `${GUIDES_URL}/using-api-with-claudecode/`,
			title: 'Using the API with Claude Code',
			text: 'Point Claude Code at the Open LLM endpoint for agentic coding.'
		}
	];

	const tools = ['VS Code + Continue', 'Obsidian', 'LangChain', 'LlamaIndex', 'Python', 'curl'];

	onMount(() => {
		origin = window.location.origin;
	});
</script>

<svelte:head>
	<title>SciLifeLab Open LLM</title>
	<meta
		name="description"
		content="Open-weight LLMs for SciLifeLab research, running on SciLifeLab infrastructure in Sweden."
	/>
</svelte:head>

<div class="landing">
	<header class="nav">
		<a class="brand" href="/welcome">
			<span class="brand-mark" aria-hidden="true">
				<svg
					width="22"
					height="22"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2.2"
					stroke-linecap="round"
					stroke-linejoin="round"
					><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z" /></svg
				>
			</span>
			<span class="brand-text">
				<span class="brand-org">SciLifeLab</span>
				<span class="brand-name">Open LLM</span>
			</span>
			<span class="pill">Pilot</span>
		</a>
		<nav class="nav-links" aria-label="Main">
			<a class="nav-link" href="{GUIDES_URL}/">Guides</a>
			<a class="nav-link" href="{GUIDES_URL}/announcement/">Announcements</a>
			<a class="nav-link" href={USE_POLICY_URL}>Use policy</a>
			<a class="btn btn-lime btn-sm" href={primaryHref}>
				{signedIn ? 'Open chat' : 'Log in'}
				<svg
					width="16"
					height="16"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2.4"
					stroke-linecap="round"
					stroke-linejoin="round"
					aria-hidden="true"><path d="M5 12h14" /><path d="m12 5 7 7-7 7" /></svg
				>
			</a>
		</nav>
	</header>

	<main id="main-content">
		<section class="hero">
			<div class="hero-copy">
				<span class="eyebrow eyebrow-lime">Language models for SciLifeLab research</span>
				<h1>Open-weight LLMs, running on our own infrastructure in Sweden.</h1>
				<p class="lead">
					SciLifeLab Open LLM gives you an OpenAI-compatible API and a web chat for open-weight
					models. Plug it into your scripts, notebooks, editors and agents — with no third-party
					providers and no training on your data.
				</p>
				<div class="actions">
					<a class="btn btn-lime btn-lg" href={primaryHref}>
						{primaryLabel}
						<svg
							width="18"
							height="18"
							viewBox="0 0 24 24"
							fill="none"
							stroke="currentColor"
							stroke-width="2.4"
							stroke-linecap="round"
							stroke-linejoin="round"
							aria-hidden="true"><path d="M5 12h14" /><path d="m12 5 7 7-7 7" /></svg
						>
					</a>
					<a class="btn btn-outline btn-lg" href="{GUIDES_URL}/getting-started-api/">
						Get started with the API
					</a>
				</div>
				{#if !signedIn}
					<p class="hint">
						New here? Register on the login page, then complete the short onboarding survey.
					</p>
				{/if}
			</div>

			<div class="code-card">
				<div class="code-bar">
					<span class="dots" aria-hidden="true"><span></span><span></span><span></span></span>
					<span class="code-name">first-request.sh</span>
				</div>
				<pre><code
						><span class="c-comment"># OpenAI-compatible chat completion</span>
curl {origin}/api/chat/completions \
  -H "Authorization: Bearer $OPEN_LLM_API_KEY" \
  -H "Content-Type: application/json" \
  -d '&#123;
    "model": "<span class="c-accent">gemma3-27b</span>",
    "messages": [
      &#123;"role": "user",
       "content": "Summarise this protocol"&#125;
    ]
  &#125;'</code
					></pre>
			</div>
		</section>

		<section class="facts">
			<div class="fact">
				<svg
					width="32"
					height="32"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					aria-hidden="true"
					><path d="M20 10c0 6-8 12-8 12s-8-6-8-12a8 8 0 0 1 16 0Z" /><circle
						cx="12"
						cy="10"
						r="3"
					/></svg
				>
				<h3>Hosted in Sweden</h3>
				<p>Runs on the KTH Kubernetes cluster and Safespring cloud, under SciLifeLab control.</p>
			</div>
			<div class="fact">
				<svg
					width="32"
					height="32"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					aria-hidden="true"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z" /></svg
				>
				<h3>No third parties</h3>
				<p>
					All processing happens on SciLifeLab-controlled infrastructure. Your data stays with us.
				</p>
			</div>
			<div class="fact">
				<svg
					width="32"
					height="32"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					aria-hidden="true"
					><rect x="3" y="11" width="18" height="11" rx="2" /><path
						d="M7 11V7a5 5 0 0 1 10 0v4"
					/></svg
				>
				<h3>No training on your data</h3>
				<p>Prompts are not used to train models. Only anonymised usage metrics are collected.</p>
			</div>
			<div class="fact">
				<svg
					width="32"
					height="32"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2"
					stroke-linecap="round"
					stroke-linejoin="round"
					aria-hidden="true"
					><polyline points="16 18 22 12 16 6" /><polyline points="8 6 2 12 8 18" /></svg
				>
				<h3>OpenAI-compatible</h3>
				<p>Point any OpenAI-compatible client at the service — no code rewrites needed.</p>
			</div>
		</section>

		<section class="section">
			<div class="section-head">
				<span class="eyebrow">Models</span>
				<h2>Capable open-weight models, ready to use</h2>
				<p>Pick a model per request through the API, or switch between them in the web chat.</p>
			</div>
			<div class="grid-2">
				<div class="model model-default">
					<div class="model-head">
						<span class="model-name">Gemma3-27b</span>
						<span class="badge">Default</span>
					</div>
					<p>
						A general-purpose model that handles both text and images — a solid choice for
						summarising, drafting, extraction and figure description.
					</p>
					<div class="tags"><span>Text</span><span>Images</span></div>
				</div>
				<div class="model">
					<div class="model-head">
						<span class="model-name">Qwen3.6-35B-A3B-FP8</span>
					</div>
					<p>
						A mixture-of-experts model well suited to coding and agentic workflows, including use
						with coding agents such as QwenCode and Claude Code.
					</p>
					<div class="tags"><span>Text</span><span>Coding agents</span></div>
				</div>
			</div>
		</section>

		<section class="section section-tint">
			<div class="section-head-row">
				<div class="section-head">
					<span class="eyebrow">Works with your tools</span>
					<h2>Built for research workflows, not just chat</h2>
					<p>The guides walk you through connecting popular tools and making your first request.</p>
				</div>
				<a class="text-link" href="{GUIDES_URL}/">
					Browse all guides
					<svg
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2.4"
						stroke-linecap="round"
						stroke-linejoin="round"
						aria-hidden="true"><path d="M5 12h14" /><path d="m12 5 7 7-7 7" /></svg
					>
				</a>
			</div>
			<div class="grid-3">
				{#each guides as guide}
					<a class="guide" href={guide.href}>
						<span class="guide-title">{guide.title}</span>
						<span class="guide-text">{guide.text}</span>
					</a>
				{/each}
			</div>
			<div class="chips">
				<span class="chips-label">Also covered:</span>
				{#each tools as tool}
					<span class="chip">{tool}</span>
				{/each}
			</div>
		</section>

		<section class="section">
			<div class="section-head">
				<span class="eyebrow">Getting access</span>
				<h2>From sign-up to first request in a day</h2>
				<p>
					The pilot is open to staff at SciLifeLab infrastructure units and members of affiliated
					research groups.
				</p>
			</div>
			<ol class="steps">
				<li class="step step-lime">
					<span class="step-num">01</span>
					<h3>Register</h3>
					<p>Create your account on the <a href="/auth">Open LLM login page</a>.</p>
				</li>
				<li class="step step-aqua">
					<span class="step-num">02</span>
					<h3>Complete onboarding</h3>
					<p>
						Fill in the three-minute onboarding survey so we understand how you plan to use the
						service.
					</p>
				</li>
				<li class="step step-teal">
					<span class="step-num">03</span>
					<h3>Get your API key</h3>
					<p>
						Once approved — usually within 24 hours — find your key under Settings → Account → API
						Keys.
					</p>
				</li>
			</ol>
		</section>

		<section class="policy grid-2">
			<div class="policy-card policy-yes">
				<h3>Good fit for</h3>
				<ul>
					<li>Internal code and non-public datasets</li>
					<li>Personal data that is not healthcare data</li>
					<li>Research workflows and agentic tools via the API</li>
					<li>Evaluating models for research purposes</li>
				</ul>
			</div>
			<div class="policy-card policy-no">
				<h3>Not for</h3>
				<ul>
					<li>Patient data, or data classified above internal</li>
					<li>Production workloads that need guaranteed uptime</li>
					<li>Heavy sustained workloads that could degrade the service</li>
					<li>Anything that breaks Swedish law, EU regulations or institutional policies</li>
				</ul>
				<a class="text-link text-link-grape" href={USE_POLICY_URL}>
					Read the full use policy
					<svg
						width="16"
						height="16"
						viewBox="0 0 24 24"
						fill="none"
						stroke="currentColor"
						stroke-width="2.4"
						stroke-linecap="round"
						stroke-linejoin="round"
						aria-hidden="true"><path d="M5 12h14" /><path d="m12 5 7 7-7 7" /></svg
					>
				</a>
			</div>
		</section>

		<section class="pilot">
			<div>
				<span class="eyebrow eyebrow-grape">This is a pilot</span>
				<h2>Help shape SciLifeLab's LLM service</h2>
				<p>
					There is no SLA during the pilot, and uptime is not guaranteed. In return, your feedback —
					through the onboarding survey and two check-ins — directly shapes what comes next.
				</p>
			</div>
			<a class="btn btn-lime btn-lg" href={primaryHref}>
				{signedIn ? 'Open the chat' : 'Log in or register'}
				<svg
					width="18"
					height="18"
					viewBox="0 0 24 24"
					fill="none"
					stroke="currentColor"
					stroke-width="2.4"
					stroke-linecap="round"
					stroke-linejoin="round"
					aria-hidden="true"><path d="M5 12h14" /><path d="m12 5 7 7-7 7" /></svg
				>
			</a>
		</section>
	</main>

	<footer class="footer">
		<div class="footer-brand">
			<span class="footer-name">SciLifeLab Open LLM</span>
			<span>Questions or feedback? <a href="mailto:{CONTACT_EMAIL}">{CONTACT_EMAIL}</a></span>
		</div>
		<nav class="footer-links" aria-label="Footer">
			<a href="{GUIDES_URL}/">Guides</a>
			<a href="{GUIDES_URL}/announcement/">Announcements</a>
			<a href={USE_POLICY_URL}>Use policy</a>
			<a class="footer-login" href={primaryHref}>{signedIn ? 'Open chat' : 'Log in'}</a>
		</nav>
	</footer>
</div>

<style>
	/* SciLifeLab graphic profile */
	.landing {
		--lime: #a7c947;
		--lime-25: #e9f2d1;
		--teal: #045c64;
		--teal-dark: #033f45;
		--teal-ink: #062a2e;
		--aqua: #4c979f;
		--aqua-25: #d2e5e7;
		--grape: #491f53;
		--grape-25: #ece6ed;
		--ink: #1c2b2d;
		--body: #33474a;
		--line: #d5e3e4;

		/* html has overflow hidden globally, so the page scrolls itself */
		position: fixed;
		inset: 0;
		overflow-y: auto;
		display: flex;
		flex-direction: column;
		background: #fff;
		color: var(--ink);
		font-family: Lato, 'Helvetica Neue', Arial, sans-serif;
		line-height: 1.5;
		word-break: normal;
	}

	.landing :global(*) {
		box-sizing: border-box;
	}

	a {
		color: var(--teal);
	}
	a:hover {
		color: var(--teal-dark);
	}

	h1,
	h2,
	h3,
	p {
		margin: 0;
	}

	/* Nav */
	.nav {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 24px;
		padding: 20px clamp(16px, 6vw, 96px);
		background: var(--teal);
		color: #fff;
		flex-wrap: wrap;
	}
	.brand {
		display: flex;
		align-items: center;
		gap: 14px;
		color: #fff;
		text-decoration: none;
	}
	.brand:hover {
		color: #fff;
	}
	.brand-mark {
		width: 40px;
		height: 40px;
		border-radius: 8px;
		background: var(--lime);
		color: var(--teal);
		display: flex;
		align-items: center;
		justify-content: center;
	}
	.brand-text {
		display: flex;
		flex-direction: column;
	}
	.brand-org {
		font-size: 13px;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: var(--lime);
	}
	.brand-name {
		font-size: 20px;
		font-weight: 900;
		line-height: 1.1;
	}
	.pill {
		padding: 4px 10px;
		border: 1px solid var(--lime);
		border-radius: 999px;
		font-size: 12px;
		font-weight: 700;
		letter-spacing: 0.04em;
		text-transform: uppercase;
		color: var(--lime);
	}
	.nav-links {
		display: flex;
		align-items: center;
		gap: 32px;
		font-size: 16px;
		font-weight: 700;
	}
	.nav-link {
		color: #fff;
		text-decoration: none;
	}
	.nav-link:hover {
		color: var(--lime);
	}

	/* Buttons */
	.btn {
		display: inline-flex;
		align-items: center;
		justify-content: center;
		gap: 10px;
		border-radius: 6px;
		text-decoration: none;
		font-weight: 900;
		white-space: nowrap;
	}
	.btn-sm {
		min-height: 44px;
		padding: 0 22px;
		font-size: 16px;
	}
	.btn-lg {
		min-height: 56px;
		padding: 0 30px;
		font-size: 18px;
	}
	.btn-lime,
	.btn-lime:hover {
		background: var(--lime);
		color: #10262a;
	}
	.btn-lime:hover {
		background: #b8d65e;
	}
	.btn-outline {
		border: 2px solid #fff;
		color: #fff;
		font-weight: 700;
	}
	.btn-outline:hover {
		background: rgba(255, 255, 255, 0.1);
		color: #fff;
	}

	/* Hero */
	.hero {
		display: grid;
		grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
		gap: 72px;
		align-items: center;
		padding: 96px clamp(16px, 6vw, 96px) 112px;
		background: var(--teal);
		color: #fff;
	}
	.hero-copy {
		display: flex;
		flex-direction: column;
		gap: 28px;
	}
	.hero h1 {
		font-size: clamp(38px, 4.4vw, 64px);
		line-height: 1.05;
		font-weight: 900;
		letter-spacing: -0.01em;
	}
	.lead {
		font-size: 21px;
		line-height: 1.55;
		color: #d9ecee;
		max-width: 580px;
	}
	.actions {
		display: flex;
		flex-wrap: wrap;
		gap: 16px;
		padding-top: 8px;
	}
	.hint {
		font-size: 15px;
		color: #bcd9dc;
	}

	.code-card {
		border-radius: 12px;
		background: var(--teal-ink);
		border: 1px solid #1d5a61;
		overflow: hidden;
		min-width: 0;
	}
	.code-bar {
		display: flex;
		align-items: center;
		justify-content: space-between;
		padding: 14px 20px;
		border-bottom: 1px solid #1d5a61;
	}
	.dots {
		display: flex;
		gap: 8px;
	}
	.dots span {
		width: 10px;
		height: 10px;
		border-radius: 50%;
		background: var(--aqua);
	}
	.code-name {
		font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
		font-size: 13px;
		color: #9cc3c7;
	}
	.code-card pre {
		margin: 0;
		padding: 28px;
		overflow-x: auto;
		font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
		font-size: 15px;
		line-height: 1.7;
		color: #e6f2f3;
	}
	.c-comment {
		color: #7fa9ad;
	}
	.c-accent {
		color: var(--lime);
	}

	/* Facts */
	.facts {
		display: grid;
		grid-template-columns: repeat(4, minmax(0, 1fr));
		gap: 32px;
		padding: 64px clamp(16px, 6vw, 96px);
		background: var(--lime-25);
	}
	.fact {
		display: flex;
		flex-direction: column;
		gap: 12px;
		color: var(--teal);
	}
	.fact h3 {
		font-size: 20px;
		font-weight: 900;
	}
	.fact p {
		font-size: 16px;
		line-height: 1.55;
		color: var(--body);
	}

	/* Sections */
	.section {
		display: flex;
		flex-direction: column;
		gap: 40px;
		padding: 96px clamp(16px, 6vw, 96px);
	}
	.section-tint {
		background: #f3f7f7;
	}
	.section-head {
		display: flex;
		flex-direction: column;
		gap: 14px;
		max-width: 760px;
	}
	.section-head h2 {
		font-size: clamp(30px, 3vw, 44px);
		line-height: 1.1;
		font-weight: 900;
		color: var(--teal);
	}
	.section-head p {
		font-size: 19px;
		line-height: 1.55;
		color: var(--body);
	}
	.section-head-row {
		display: flex;
		align-items: flex-end;
		justify-content: space-between;
		gap: 24px 48px;
		flex-wrap: wrap;
	}
	.eyebrow {
		font-size: 15px;
		font-weight: 700;
		letter-spacing: 0.08em;
		text-transform: uppercase;
		color: #3a7a81;
	}
	.eyebrow-lime {
		color: var(--lime);
	}
	.eyebrow-grape {
		color: #d9c7dd;
	}
	.text-link {
		display: inline-flex;
		align-items: center;
		gap: 8px;
		min-height: 44px;
		font-size: 17px;
		font-weight: 900;
		white-space: nowrap;
	}
	.text-link-grape,
	.text-link-grape:hover {
		color: var(--grape);
	}

	.grid-2 {
		display: grid;
		grid-template-columns: repeat(2, minmax(0, 1fr));
		gap: 32px;
	}
	.grid-3 {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 24px;
	}

	/* Models */
	.model {
		display: flex;
		flex-direction: column;
		gap: 16px;
		padding: 36px;
		border-radius: 12px;
		border: 2px solid #c9dadc;
		background: #fff;
	}
	.model-default {
		border-color: var(--teal);
	}
	.model-head {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 12px;
		flex-wrap: wrap;
	}
	.model-name {
		font-family: ui-monospace, 'JetBrains Mono', Menlo, monospace;
		font-size: 22px;
		font-weight: 500;
		color: var(--teal);
		overflow-wrap: anywhere;
	}
	.badge {
		padding: 5px 12px;
		border-radius: 999px;
		background: var(--teal);
		color: #fff;
		font-size: 13px;
		font-weight: 700;
	}
	.model p {
		font-size: 17px;
		line-height: 1.55;
		color: var(--body);
	}
	.tags {
		display: flex;
		gap: 8px;
		flex-wrap: wrap;
	}
	.tags span {
		padding: 6px 12px;
		border-radius: 6px;
		background: var(--aqua-25);
		color: var(--teal-dark);
		font-size: 14px;
		font-weight: 700;
	}

	/* Guides */
	.guide {
		display: flex;
		flex-direction: column;
		gap: 10px;
		padding: 28px;
		border-radius: 10px;
		background: #fff;
		border: 1px solid var(--line);
		text-decoration: none;
	}
	.guide:hover {
		border-color: var(--teal);
	}
	.guide-title {
		font-size: 20px;
		font-weight: 900;
		color: var(--teal);
	}
	.guide-text {
		font-size: 16px;
		line-height: 1.55;
		color: var(--body);
	}
	.chips {
		display: flex;
		flex-wrap: wrap;
		align-items: center;
		gap: 12px;
	}
	.chips-label {
		font-size: 15px;
		font-weight: 700;
		color: var(--body);
		margin-right: 8px;
	}
	.chip {
		padding: 8px 16px;
		border-radius: 999px;
		background: #fff;
		border: 1px solid #c9dadc;
		font-size: 15px;
		font-weight: 700;
		color: var(--teal);
	}

	/* Steps */
	.steps {
		display: grid;
		grid-template-columns: repeat(3, minmax(0, 1fr));
		gap: 32px;
		margin: 0;
		padding: 0;
		list-style: none;
	}
	.step {
		display: flex;
		flex-direction: column;
		gap: 16px;
		padding-top: 24px;
		border-top: 4px solid var(--teal);
	}
	.step-num {
		font-size: 44px;
		font-weight: 900;
		line-height: 1;
		color: var(--teal);
	}
	.step-lime {
		border-color: var(--lime);
	}
	.step-lime .step-num {
		color: #7f9c2c;
	}
	.step-aqua {
		border-color: var(--aqua);
	}
	.step-aqua .step-num {
		color: var(--aqua);
	}
	.step h3 {
		font-size: 22px;
		font-weight: 900;
		color: var(--teal);
	}
	.step p {
		font-size: 17px;
		line-height: 1.55;
		color: var(--body);
	}
	.step a {
		font-weight: 700;
	}

	/* Policy */
	.policy {
		padding: 0 clamp(16px, 6vw, 96px) 96px;
	}
	.policy-card {
		display: flex;
		flex-direction: column;
		gap: 20px;
		padding: 40px;
		border-radius: 12px;
	}
	.policy-card h3 {
		font-size: 24px;
		font-weight: 900;
	}
	.policy-card ul {
		margin: 0;
		padding-left: 22px;
		display: flex;
		flex-direction: column;
		gap: 12px;
		font-size: 17px;
		line-height: 1.5;
		list-style: disc;
	}
	.policy-yes {
		background: var(--lime-25);
	}
	.policy-yes h3 {
		color: var(--teal);
	}
	.policy-no {
		background: var(--grape-25);
	}
	.policy-no h3 {
		color: var(--grape);
	}

	/* Pilot banner */
	.pilot {
		display: flex;
		align-items: center;
		justify-content: space-between;
		gap: 32px 64px;
		flex-wrap: wrap;
		margin: 0 clamp(16px, 6vw, 96px) 96px;
		padding: 56px clamp(24px, 4vw, 64px);
		border-radius: 16px;
		background: var(--grape);
		color: #fff;
	}
	.pilot > div {
		display: flex;
		flex-direction: column;
		gap: 14px;
		max-width: 760px;
	}
	.pilot h2 {
		font-size: clamp(28px, 2.6vw, 36px);
		line-height: 1.15;
		font-weight: 900;
	}
	.pilot p {
		font-size: 18px;
		line-height: 1.55;
		color: #eadfec;
	}

	/* Footer */
	.footer {
		margin-top: auto;
		display: flex;
		justify-content: space-between;
		align-items: flex-start;
		gap: 24px 48px;
		flex-wrap: wrap;
		padding: 56px clamp(16px, 6vw, 96px);
		background: var(--teal-ink);
		color: #cfe3e5;
		font-size: 15px;
	}
	.footer-brand {
		display: flex;
		flex-direction: column;
		gap: 10px;
	}
	.footer-name {
		font-size: 20px;
		font-weight: 900;
		color: #fff;
	}
	.footer a {
		color: #fff;
		font-weight: 700;
	}
	.footer-brand a,
	.footer .footer-login {
		color: var(--lime);
	}
	.footer-links {
		display: flex;
		gap: 16px 32px;
		flex-wrap: wrap;
	}

	/* Responsive */
	@media (max-width: 1100px) {
		.hero {
			grid-template-columns: minmax(0, 1fr);
			gap: 48px;
			padding-top: 64px;
			padding-bottom: 72px;
		}
		.facts {
			grid-template-columns: repeat(2, minmax(0, 1fr));
		}
		.grid-3,
		.steps {
			grid-template-columns: minmax(0, 1fr);
		}
	}

	@media (max-width: 760px) {
		.nav-link {
			display: none;
		}
		.facts,
		.grid-2 {
			grid-template-columns: minmax(0, 1fr);
		}
		.section {
			padding-top: 64px;
			padding-bottom: 64px;
		}
		.lead {
			font-size: 18px;
		}
		.code-card pre {
			padding: 20px;
			font-size: 13px;
		}
		.model,
		.policy-card {
			padding: 28px;
		}
		.btn-lg {
			width: 100%;
		}
	}
</style>
