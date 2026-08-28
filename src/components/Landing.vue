<template>
  <div class="landing">
    <header class="landing-nav">
      <div class="landing-brand">
        <md-icon>insights</md-icon>
        <span>Financial Dashboard</span>
      </div>
      <router-link to="/login" class="landing-nav-link">Log in</router-link>
    </header>

    <section class="hero">
      <div class="hero-copy">
        <span class="eyebrow">Personal portfolio intelligence</span>
        <h1 class="hero-title">Every holding.<br>Every tick.<br><em>One dashboard.</em></h1>
        <p class="hero-subtitle">
          Track what your portfolio is actually worth, compare any two tickers side by side,
          and see market moves the moment they happen — all in one place, built for people who
          check their portfolio more than once a day.
        </p>
        <div class="hero-actions">
          <router-link to="/register">
            <md-button class="md-raised hero-cta-primary">Create free account</md-button>
          </router-link>
          <router-link to="/login">
            <md-button class="md-raised hero-cta-secondary">Log in</md-button>
          </router-link>
        </div>
      </div>

      <div class="ticker-tape" aria-hidden="true">
        <div class="ticker-tape-track">
          <div class="ticker-tape-card up fin" v-for="n in 2" :key="`spx-${n}`">
            <span class="tt-label">S&amp;P 500</span>
            <span class="tt-price">5,943.12</span>
            <span class="tt-change">+0.84%</span>
          </div>
          <div class="ticker-tape-card down fin" v-for="n in 2" :key="`nasdaq-${n}`">
            <span class="tt-label">NASDAQ</span>
            <span class="tt-price">19,281.45</span>
            <span class="tt-change">&minus;0.42%</span>
          </div>
          <div class="ticker-tape-card up fin" v-for="n in 2" :key="`aapl-${n}`">
            <span class="tt-label">AAPL</span>
            <span class="tt-price">312.44</span>
            <span class="tt-change">+1.86%</span>
          </div>
          <div class="ticker-tape-card up fin" v-for="n in 2" :key="`gold-${n}`">
            <span class="tt-label">GOLD</span>
            <span class="tt-price">2,415.60</span>
            <span class="tt-change">+1.12%</span>
          </div>
          <div class="ticker-tape-card down fin" v-for="n in 2" :key="`eurusd-${n}`">
            <span class="tt-label">EUR/USD</span>
            <span class="tt-price">1.0842</span>
            <span class="tt-change">&minus;0.18%</span>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="feature">
        <div class="feature-icon"><md-icon>show_chart</md-icon></div>
        <h3>Track performance, not guesses</h3>
        <p>
          Every holding's real gain or loss over time, weighed against what you actually paid —
          not just today's price.
        </p>
      </div>
      <div class="feature">
        <div class="feature-icon"><md-icon>compare_arrows</md-icon></div>
        <h3>Compare any two tickers</h3>
        <p>
          Line up any symbols against each other across any timeframe before you decide
          where the next dollar goes.
        </p>
      </div>
      <div class="feature">
        <div class="feature-icon"><md-icon>public</md-icon></div>
        <h3>Markets, at a glance</h3>
        <p>
          Indices, commodities, and FX in one live strip, so you know what's moving before
          you even open a position.
        </p>
      </div>
    </section>

    <section class="final-cta">
      <h2>Set it up in under a minute.</h2>
      <router-link to="/register">
        <md-button class="md-raised hero-cta-primary">Create free account</md-button>
      </router-link>
    </section>

    <footer class="landing-footer">
      <span>Financial Dashboard</span>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'Landing',
};
</script>

<style scoped>
.landing {
  font-family: 'IBM Plex Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  color: #eaf3f1;
}

.fin {
  font-family: 'JetBrains Mono', ui-monospace, monospace;
  font-variant-numeric: tabular-nums;
}

/* ---------- nav ---------- */
.landing-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1180px;
  margin: 0 auto;
  padding: 28px 24px 0;
}
.landing-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-weight: 600;
  letter-spacing: 0.01em;
}
.landing-brand :deep(.md-icon) {
  color: #2fd8d4 !important;
  font-size: 22px !important;
}
.landing-nav-link {
  color: rgba(234, 243, 241, 0.8);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}
.landing-nav-link:hover {
  color: #fff;
}

/* ---------- hero ---------- */
.hero {
  background: radial-gradient(ellipse 900px 500px at 20% 0%, rgba(0, 170, 173, 0.25), transparent 60%),
    linear-gradient(160deg, #051617 0%, #0c2a2c 55%, #114347 100%);
  padding: 64px 24px 0;
}
.hero-copy {
  max-width: 1180px;
  margin: 0 auto;
  padding-bottom: 56px;
  text-align: left;
}
.eyebrow {
  display: inline-block;
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #2fd8d4;
  margin-bottom: 20px;
}
.hero-title {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 700;
  font-size: 64px;
  line-height: 1.08;
  margin: 0 0 24px;
  max-width: 720px;
  text-wrap: balance;
}
.hero-title em {
  font-style: italic;
  font-weight: 600;
  color: #2fd8d4;
}
.hero-subtitle {
  max-width: 560px;
  font-size: 17px;
  line-height: 1.6;
  color: rgba(234, 243, 241, 0.72);
  margin: 0 0 36px;
}
.hero-actions {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}
.hero-cta-primary {
  background-color: #2fd8d4 !important;
  color: #06282a !important;
  font-weight: 700 !important;
}
.hero-cta-secondary {
  background-color: transparent !important;
  color: #fff !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: none !important;
}

/* ---------- ticker tape (signature element) ---------- */
.ticker-tape {
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  overflow: hidden;
  padding: 20px 0;
}
.ticker-tape-track {
  display: flex;
  gap: 16px;
  width: max-content;
  animation: ticker-scroll 32s linear infinite;
}
@keyframes ticker-scroll {
  from {
    transform: translateX(0);
  }
  to {
    transform: translateX(-50%);
  }
}
@media (prefers-reduced-motion: reduce) {
  .ticker-tape-track {
    animation: none;
  }
}
.ticker-tape-card {
  flex-shrink: 0;
  display: flex;
  align-items: baseline;
  gap: 10px;
  padding: 10px 18px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.08);
  font-size: 13px;
  white-space: nowrap;
}
.tt-label {
  font-weight: 600;
  color: rgba(234, 243, 241, 0.6);
}
.tt-price {
  font-weight: 600;
  color: #fff;
}
.ticker-tape-card.up .tt-change {
  color: #33c98f;
}
.ticker-tape-card.down .tt-change {
  color: #ef6b83;
}

/* ---------- features ---------- */
.features {
  background: #f5f7f6;
  color: #0f2224;
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 32px;
  max-width: 1180px;
  margin: 0 auto;
  padding: 72px 24px;
  text-align: left;
}
.feature-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: rgba(17, 100, 104, 0.1);
  color: #116468;
  margin-bottom: 16px;
}
.feature-icon :deep(.md-icon) {
  color: #116468 !important;
}
.feature h3 {
  margin: 0 0 8px;
  font-size: 18px;
}
.feature p {
  margin: 0;
  color: rgba(15, 34, 36, 0.65);
  font-size: 14px;
  line-height: 1.6;
}

/* ---------- final CTA ---------- */
.final-cta {
  background: #116468;
  color: #fff;
  text-align: center;
  padding: 64px 24px;
}
.final-cta h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  font-size: 30px;
  margin: 0 0 28px;
}

/* ---------- footer ---------- */
.landing-footer {
  background: #0a383a;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  padding: 20px;
  font-size: 13px;
}

@media (max-width: 900px) {
  .hero-title {
    font-size: 44px;
  }
  .features {
    grid-template-columns: 1fr;
  }
}
</style>
