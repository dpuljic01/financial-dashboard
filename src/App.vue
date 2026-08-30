<template>
  <div id="app">
    <navigation v-if="protectedRoutes.includes(this.$route.name)" />
    <router-view v-else></router-view>
    <Toaster
      position="top-center"
      rich-colors
      close-button
      theme="light"
      :offset="{ top: '84px' }"
      :mobile-offset="{ top: '84px' }"
    />
  </div>
</template>

<script>
import { Toaster } from 'vue-sonner';
import { PROTECTED_ROUTES } from './consts';

export default {
  components: {
    Toaster,
  },
  data() {
    return {
      protectedRoutes: PROTECTED_ROUTES,
    };
  },
};
</script>
<style>
/* Safety net: nothing on this site is meant to scroll horizontally at the
   page level (wide tables/ticker strips already scroll internally via
   their own overflow-x). Without this, any element even 1px wider than
   the viewport - a rounding error in a flex row, a chart canvas that
   hasn't resized yet - makes the whole page scrollable sideways on
   mobile, which is what "can scroll right a bit on Dashboard" was. */
html,
body {
  overflow-x: hidden;
  max-width: 100%;
}

#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  text-align: center;
  color: #2c3e50;
  min-height: 100vh;
  /* This is an app UI, not a document - a long-press-to-select on a heading
     or label (triggering the OS's selection handles/dictionary popup) reads
     as broken, not helpful. Form inputs are unaffected: user-select on an
     ancestor doesn't reach into a native <input>/<textarea>'s own text. */
  -webkit-touch-callout: none;
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
  --gain-color: #0f9d70;
  --loss-color: #d1435c;
  --gain-tint: rgba(15, 157, 112, 0.12);
  --loss-tint: rgba(209, 67, 92, 0.12);
  --surface-color: #ffffff;
  --surface-border: rgba(17, 100, 104, 0.08);
  --surface-shadow: 0 2px 10px rgba(17, 40, 40, 0.06);
  --surface-shadow-hover: 0 10px 24px rgba(17, 40, 40, 0.14);
}
#app .md-app {
  min-height: 100vh;
}
h4 {
  text-align: left;
}
.md-heading,
.md-title {
  text-align: left;
}
.md-heading {
  margin: 24px 0 12px;
}

/* Tabular, monospaced figures for prices/changes/volume - reads as an
   instrument panel rather than plain body text, and digits no longer
   shift width as they tick up/down. */
.fin-figure {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  font-variant-numeric: tabular-nums;
  letter-spacing: -0.01em;
}
.fin-gain {
  color: var(--gain-color);
}
.fin-loss {
  color: var(--loss-color);
}

/* Shared page/card scaffolding so every page reads as one system instead
   of ad hoc per-component spacing. */
.page-container {
  max-width: 1180px;
  margin: 0 auto;
  text-align: left;
}
.page-section {
  margin-bottom: 44px;
}
.page-section:last-child {
  margin-bottom: 0;
}
.card-surface {
  background: var(--surface-color);
  border: 1px solid var(--surface-border);
  border-radius: 16px;
  box-shadow: var(--surface-shadow);
}
</style>
