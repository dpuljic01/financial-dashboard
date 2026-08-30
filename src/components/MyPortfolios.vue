<template>
  <div v-if="loaded" class="page-container">
    <div v-if="portfolios.length > 0" class="page-section card-surface portfolios-card">
      <div class="portfolios-header">
        <h3 class="portfolios-title">Portfolios</h3>
        <md-button class="md-icon-button md-dense md-raised md-primary" @click="open = true">
          <md-icon>add</md-icon>
        </md-button>
      </div>
      <div class="table-scroll">
        <table class="fin-table">
          <thead>
            <tr>
              <th class="col-del"></th>
              <th>Name</th>
              <th class="num">Symbols</th>
              <th class="num">Holdings</th>
              <th class="num">Worth (USD)</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in portfolios" :key="item.id">
              <td class="col-del">
                <button type="button" class="row-action" title="Delete" @click="deletePortfolio(item.id)">
                  <md-icon>delete_outline</md-icon>
                </button>
              </td>
              <td @click="goToSummary(item.id)"><strong>{{ item.name }}</strong></td>
              <td @click="goToSummary(item.id)" class="num fin-figure">{{ item.stocks.length }}</td>
              <td @click="goToSummary(item.id)" class="num fin-figure">{{ item.holdings.length }}</td>
              <td @click="goToSummary(item.id)" class="num fin-figure">
                {{ formatCurrency(calculatePortfolioValue(item.holdings)) }}
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div v-if="portfolios.length === 0" class="empty-state">
      <strong class="empty-state-label">Create your first portfolio</strong>
      <div>
        <button type="button" class="empty-state-cta" @click="open = true">+ Create portfolio</button>
      </div>
    </div>

    <Modal v-model="open">
      <h3 class="modal-title">Create portfolio</h3>
      <form @submit.prevent="submit">
        <md-field>
          <label for="portfolioName">Portfolio name</label>
          <md-input v-model="portfolioName" name="portfolioName" id="portfolioName" autofocus></md-input>
        </md-field>
        <p class="dp-error" v-if="!valid">Must have at least two characters</p>

        <md-field>
          <label>Additional info (Optional)</label>
          <md-textarea v-model="info"></md-textarea>
        </md-field>
        <div class="modal-actions">
          <md-button class="md-raised" :disabled="submitting" @click="open = false">Cancel</md-button>
          <md-button class="md-raised md-primary" type="submit" :disabled="submitting">
            {{ submitting ? 'Creating…' : 'Save' }}
          </md-button>
        </div>
      </form>
    </Modal>
  </div>
</template>

<script>
import Modal from './Modal.vue';

export default {
  name: 'MyPortfolios',
  components: {
    Modal,
  },
  data() {
    return {
      open: false,
      submitting: false,
      portfolioName: '',
      info: '',
      valid: false,
      portfolios: [],
      loaded: false,
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    // Always refetch rather than trusting the localStorage-cached list - it
    // goes stale the moment a portfolio is added/removed from another tab,
    // session, or device, and silently under-lists portfolios here.
    this.portfolios = await this.$store.dispatch('getPortfolios');
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    goToSummary(id) {
      this.$router.push(`/portfolios/${id}/summary`);
    },
    async createPortfolio() {
      this.submitting = true;
      this.$store.commit('setLoading', true);
      try {
        const portfolio = await this.$store.dispatch('submitNewPortfolio', {
          name: this.portfolioName,
          info: this.info,
        });
        this.open = false;
        this.portfolioName = '';
        this.info = '';
        this.$router.push(`/portfolios/${portfolio.id}/summary`);
      } finally {
        this.submitting = false;
        this.$store.commit('setLoading', false);
      }
    },
    submit() {
      if (this.valid) {
        this.createPortfolio();
      }
    },
    validName(value) {
      return value.length > 1;
    },
    calculatePortfolioValue(holdings) {
      let worth = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        worth += holdings[i].price * holdings[i].shares;
      }
      return worth;
    },
    formatCurrency(val) {
      return `$${val.toFixed(2)}`;
    },
    async deletePortfolio(pId) {
      if (!window.confirm('Are you sure about that?')) return;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('deletePortfolio', { portfolioId: pId });
      this.portfolios = await this.$store.dispatch('getPortfolios');
      this.$store.commit('setLoading', false);
    },
  },
  watch: {
    portfolioName(value) {
      this.portfolioName = value;
      this.valid = this.validName(value);
    },
    portfolios(val) {
      this.portfolios = val;
    },
  },
};
</script>

<style lang="scss" scoped>
.md-card {
  text-align: left;
}

.close-icon {
  position: absolute;
  right: 4%;
}
.portfolios-card {
  padding: 28px;
}
.portfolios-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 20px;
}
.portfolios-title {
  margin: 0;
  font-size: 20px;
  font-weight: 600;
}
.table-scroll {
  overflow-x: auto;
}
.fin-table {
  width: 100%;
  min-width: 480px;
  border-collapse: collapse;
}
.fin-table th {
  text-align: left;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  color: rgba(0, 0, 0, 0.5);
  padding: 0 12px 10px 0;
}
.fin-table th.num {
  text-align: right;
}
.fin-table td {
  padding: 12px 12px 12px 0;
  border-top: 1px solid var(--surface-border);
}
.fin-table td:not(.col-del) {
  cursor: pointer;
}
.fin-table td.num {
  text-align: right;
}
.fin-table tbody tr:hover td {
  background: rgba(17, 100, 104, 0.04);
}
.col-del {
  width: 32px;
  padding-right: 0;
}
.row-action {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  padding: 0;
  border: none;
  border-radius: 50%;
  background: none;
  color: rgba(0, 0, 0, 0.35);
  cursor: pointer;
}
.row-action:hover {
  background: var(--loss-tint);
  color: var(--loss-color);
}
.row-action .md-icon {
  margin: 0;
  font-size: 18px !important;
}
.modal-title {
  margin: 0 0 16px;
}
.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 16px;
}
.empty-state {
  text-align: center;
  padding: 48px 16px;
}
.empty-state-label {
  display: block;
  font-size: 20px;
  margin-bottom: 16px;
}
.empty-state-cta {
  background: #116468;
  color: #fff;
  border: none;
  border-radius: 24px;
  padding: 12px 24px;
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.15s ease;
}
.empty-state-cta:hover {
  background: #0a383a;
}
</style>
