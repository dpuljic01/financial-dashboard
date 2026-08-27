<template>
  <div v-if="loaded">
    <div v-if="portfolios.length > 0" class="md-layout md-subheader md-size-100 md-alignment-center-space-between">
      <div class="md-size-40">
        <h3>PORTFOLIOS</h3>
      </div>
      <md-button class="md-size-40 md-fab md-mini md-primary" @click="open = true">
        <md-icon>add</md-icon>
      </md-button>
    </div>
    <table v-if="portfolios.length > 0" class="md-content tbl plain-table">
      <thead>
        <tr>
          <th class="col-del">Del</th>
          <th>Name</th>
          <th>Symbols</th>
          <th>Shares</th>
          <th>Worth (USD)</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in portfolios" :key="item.id">
          <td class="col-del">
            <md-button
              class="md-icon md-raised md-primary"
              style="background-color: #d00000;"
              @click="deletePortfolio(item.id)"
              ><md-icon>delete_outline</md-icon></md-button
            >
          </td>
          <td @click="goToSummary(item.id)">{{ item.name }}</td>
          <td @click="goToSummary(item.id)">{{ item.stocks.length }}</td>
          <td @click="goToSummary(item.id)">{{ item.holdings.length }}</td>
          <td @click="goToSummary(item.id)">{{ calculatePortfolioValue(item.holdings) }}</td>
        </tr>
      </tbody>
    </table>
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
          <md-button class="md-raised" @click="open = false">Cancel</md-button>
          <md-button class="md-raised md-primary" type="submit">Save</md-button>
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
      portfolioName: '',
      info: '',
      valid: false,
      portfolios: [],
      loaded: false,
    };
  },
  async mounted() {
    this.$store.commit('setLoading', true);
    this.portfolios = this.$store.getters.listPortfolios;
    if (this.portfolios.length === 0) {
      this.portfolios = await this.$store.dispatch('getPortfolios');
    }
    this.$store.commit('setLoading', false);
    this.loaded = true;
  },
  methods: {
    goToSummary(id) {
      this.$router.push(`/portfolios/${id}/summary`);
    },
    async createPortfolio() {
      this.open = false;
      this.$store.commit('setLoading', true);
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolios = await this.$store.dispatch('getPortfolios');
      this.portfolioName = '';
      this.info = '';
      this.$store.commit('setLoading', false);
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
      let price = 0;
      for (let i = 0; i < holdings.length; i += 1) {
        price += holdings[i].price;
      }
      return price;
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
.plain-table {
  width: 100%;
  border-collapse: collapse;
}
.plain-table th,
.plain-table td {
  text-align: center;
  padding: 8px;
  border-bottom: 1px solid rgba(0, 0, 0, 0.12);
}
.plain-table td:not(.col-del) {
  cursor: pointer;
}
.col-del {
  max-width: 40px;
  padding: 0;
  margin: 0;
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
