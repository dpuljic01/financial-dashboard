<template>
  <div class="landing">
    <section class="hero">
      <div class="hero-copy">
        <div class="landing-brand">
          <md-icon>insights</md-icon>
          <span>Financial Dashboard</span>
        </div>

        <span class="eyebrow">Personal portfolio intelligence</span>
        <h1 class="hero-title">Your portfolio,<br><em>finally in focus.</em></h1>
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

      <a class="hero-badge" :href="productHuntUrl" target="_blank" rel="noopener noreferrer">
        <img :src="productHuntBadge" :alt="productHuntAlt" width="250" height="54" loading="lazy" />
      </a>

      <div class="ticker-tape" v-if="tickers.length > 0" aria-hidden="true">
        <div class="ticker-tape-track">
          <div
            class="ticker-tape-card fin"
            :class="item.trend"
            v-for="(item, index) in tapeItems"
            :key="`${item.symbol}-${index}`"
          >
            <span class="tt-label">{{ item.label }}</span>
            <span class="tt-price">{{ item.price }}</span>
            <span class="tt-change">{{ item.change }}</span>
          </div>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="feature">
        <div class="feature-icon"><md-icon>show_chart</md-icon></div>
        <h3>Track performance</h3>
        <p>
          Every holding's real gain or loss over time, weighed against what you actually paid —
          not just today's price.
        </p>
      </div>
      <div class="feature">
        <div class="feature-icon"><md-icon>compare_arrows</md-icon></div>
        <h3>Compare multiple tickers</h3>
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

    <section class="final-cta-wrap">
      <div class="final-cta">
        <h2>Set it up in under a minute.</h2>
        <p>Create a portfolio, add what you hold, and watch it update live.</p>
        <router-link to="/register">
          <md-button class="md-raised hero-cta-primary">Create free account</md-button>
        </router-link>
        <span class="final-cta-note">No credit card required</span>
      </div>
    </section>

    <footer class="landing-footer">
      <div class="footer-content">
        <span>Financial Dashboard</span>
        <span class="divider"> • </span>
        <a href="https://www.puljic.ch" target="_blank" rel="noopener noreferrer">www.puljic.ch</a>
        <span class="divider"> • </span>
        <span>&copy; 2026 Puljic</span>
      </div>
    </footer>
  </div>
</template>

<script>
import { getMarketSnapshot } from '../api';

const SNAPSHOT_ORDER = ['^gspc', '^ixic', '^dji', 'gc=f', 'EURUSD=X'];
const SNAPSHOT_LABELS = {
  '^gspc': 'S&P 500',
  '^ixic': 'NASDAQ',
  '^dji': 'DOW 30',
  'gc=f': 'Gold',
  'EURUSD=X': 'EUR/USD',
};

const PRODUCT_HUNT_POST = 'real-time-financial-dashboard';
const PRODUCT_HUNT_POST_ID = '1240374';

export default {
  name: 'Landing',
  data() {
    return {
      tickers: [],
      productHuntUrl:
        `https://www.producthunt.com/products/${PRODUCT_HUNT_POST}?embed=true`
        + '&utm_source=badge-featured&utm_medium=badge'
        + `&utm_campaign=badge-${PRODUCT_HUNT_POST}`,
      productHuntBadge:
        `https://api.producthunt.com/widgets/embed-image/v1/featured.svg?post_id=${PRODUCT_HUNT_POST_ID}`
        + '&theme=dark',
      productHuntAlt:
        'Real-time Financial Dashboard - Track markets and spending, '
        + 'rebuilt from my 2020 MSc thesis | Product Hunt',
    };
  },
  computed: {
    // Duplicate the whole set once (not each item) so the CSS marquee can
    // loop seamlessly at translateX(-50%) without any ticker appearing
    // twice back-to-back.
    tapeItems() {
      return [...this.tickers, ...this.tickers];
    },
  },
  async mounted() {
    try {
      const resp = await getMarketSnapshot();
      this.tickers = SNAPSHOT_ORDER
        .map((symbol) => ({ symbol, quote: resp.data[symbol] }))
        .filter(({ quote }) => quote && quote.changepercent != null)
        .map(({ symbol, quote }) => {
          let trend = 'flat';
          if (quote.changepercent > 0) trend = 'up';
          else if (quote.changepercent < 0) trend = 'down';
          const sign = quote.changepercent > 0 ? '+' : '';
          return {
            symbol,
            label: SNAPSHOT_LABELS[symbol],
            price: this.formatPrice(quote.price),
            change: `${sign}${quote.changepercent.toFixed(2)}%`,
            trend,
          };
        });
    } catch (e) {
      this.tickers = [];
    }
  },
  methods: {
    formatPrice(value) {
      if (value < 10) return value.toFixed(4);
      return value.toLocaleString('en-US', { minimumFractionDigits: 2, maximumFractionDigits: 2 });
    },
  },
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

/* ---------- brand ---------- */
.landing-brand {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 17px;
  font-weight: 700;
  letter-spacing: 0.01em;
  margin-bottom: 40px;
  line-height: 1;
}
.landing-brand :deep(.md-icon) {
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  width: 26px;
  height: 26px;
  margin: 0 !important;
  color: #2fd8d4 !important;
  font-size: 24px !important;
  line-height: 1 !important;
  flex-shrink: 0;
}

/* ---------- hero ---------- */
.hero {
  position: relative;
  background-color: #051617;
  background-image:
    url('../assets/hero-pattern.svg'),
    radial-gradient(ellipse 900px 500px at 20% 0%, rgba(0, 170, 173, 0.25), transparent 60%),
    linear-gradient(160deg, #051617 0%, #0c2a2c 55%, #114347 100%);
  background-repeat: repeat, no-repeat, no-repeat;
  background-size: 240px 240px, auto, auto;
  padding: 56px 24px 0;
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
.hero-badge {
  position: absolute;
  right: 24px;
  bottom: 24px;
  width: 190px;
}
.hero-badge img {
  display: block;
  width: 100%;
  height: auto;
}
@media (max-width: 720px) {
  .hero-badge {
    position: static;
    margin: 20px 0 0;
  }
}
.hero-cta-primary {
  background-color: #e2a54d !important;
  color: #2b1608 !important;
  font-weight: 700 !important;
}
.hero-cta-secondary {
  background-color: transparent !important;
  color: #fff !important;
  border: 1px solid rgba(255, 255, 255, 0.3) !important;
  box-shadow: none !important;
}

/* ---------- ticker tape (signature element, real live data) ---------- */
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
.final-cta-wrap {
  background: #f5f7f6;
  padding: 0 24px 80px;
}
.final-cta {
  max-width: 880px;
  margin: 0 auto;
  border-radius: 24px;
  padding: 64px 40px;
  text-align: center;
  color: #fff;
  background: radial-gradient(ellipse 700px 400px at 50% 0%, rgba(47, 216, 212, 0.18), transparent 60%),
    linear-gradient(160deg, #051617 0%, #0c2a2c 55%, #114347 100%);
}
.final-cta h2 {
  font-family: 'Fraunces', Georgia, serif;
  font-weight: 600;
  font-size: 32px;
  margin: 0 0 12px;
}
.final-cta p {
  margin: 0 0 28px;
  color: rgba(234, 243, 241, 0.72);
  font-size: 15px;
}
.final-cta-note {
  display: block;
  margin-top: 14px;
  font-size: 12px;
  color: rgba(234, 243, 241, 0.5);
}

/* ---------- footer ---------- */
.landing-footer {
  background: #f5f7f6;
  color: rgba(15, 34, 36, 0.45);
  text-align: center;
  padding: 8px 24px 28px;
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
