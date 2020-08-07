<template>
  <div>
    <md-empty-state
      md-icon="post_add"
      md-label="Create your first portfolio"
      md-description="By creating a portfolio, you'll be able to add your holdings and get valuable information."
    >
      <!--<md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>-->
      <md-button class="md-primary md-raised" @click="open = true">Create portfolio</md-button>
    </md-empty-state>
    <md-dialog :md-active.sync="open">
      <md-dialog-title
        >Create portfolio
        <md-button class="md-icon" @click="open = false">close</md-button>
      </md-dialog-title>
      <md-dialog-content>
        <form novalidate @submit.prevent="submit">
          <md-field>
            <label for="portfolioName">Portfolio name</label>
            <md-input v-model="portfolioName" name="portfolioName" id="portfolioName" autofocus></md-input>
          </md-field>
          <p class="dp-error" v-if="!valid">Must have at least two characters</p>

          <md-field>
            <label>Additional info (Optional)</label>
            <md-textarea v-model="info"></md-textarea>
          </md-field>
          <md-dialog-actions>
            <md-button class="md-raised" @click="open = false">Cancel</md-button>
            <md-button class="md-raised md-primary" type="submit">Save</md-button>
          </md-dialog-actions>
        </form>
      </md-dialog-content>
      <!-- <md-steppers :md-active-step.sync="active" md-linear>
        <md-step id="first" md-label="Info" :md-error="firstStepError" :md-done.sync="first">
          <md-field>
            <label for="portfolioName">Portfolio name</label>
            <md-input v-model="portfolioName" name="portfolioName" id="portfolioName" autofocus></md-input>
          </md-field>

          <md-field>
            <label>Additional info</label>
            <md-textarea v-model="info"></md-textarea>
          </md-field>

          <p class="dp-error" v-if="msg.firstName">Must have at least two characters</p>
          <md-button class="md-raised md-primary" :disabled="portfolioName === ''" @click="setDone('first', 'second')"
            >Continue</md-button
          >
        </md-step>

        <md-step id="second" md-label="Holdings" :md-error="secondStepError" :md-done.sync="second">
          <md-table v-for="row in tableData" :key="row.id">
            <md-table-row>
              <md-table-head md-numeric>ID</md-table-head>
              <md-table-head>Name</md-table-head>
              <md-table-head>Email</md-table-head>
              <md-table-head>Gender</md-table-head>
              <md-table-head>Job Title</md-table-head>
            </md-table-row>
          </md-table>
          <md-button class="md-raised" @click="setDone('second', 'third')">Continue</md-button>
        </md-step>

        <md-step id="third" md-label="Review" :md-done.sync="third">
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestias doloribus eveniet quaerat modi cumque
            quos sed, temporibus nemo eius amet aliquid, illo minus blanditiis tempore, dolores voluptas dolore placeat
            nulla.
          </p>
          <p>
            Lorem ipsum dolor sit amet consectetur adipisicing elit. Molestias doloribus eveniet quaerat modi cumque
            quos sed, temporibus nemo eius amet aliquid, illo minus blanditiis tempore, dolores voluptas dolore placeat
            nulla.
          </p>
          <md-button class="md-raised" @click="onConfirm()">Looks good!</md-button>
        </md-step>
      </md-steppers> -->
    </md-dialog>
  </div>
</template>

<script>
export default {
  name: 'Portfolio',
  data() {
    return {
      open: false,
      portfolioName: '',
      info: '',
      valid: false,
    };
  },
  methods: {
    async createPortfolio() {
      this.open = false;
      this.$store.state.loading = true;
      await this.$store.dispatch('submitNewPortfolio', { name: this.portfolioName, info: this.info });
      this.portfolioName = '';
      this.info = '';
    },
    submit() {
      if (this.valid) {
        this.createPortfolio();
      }
    },
    validName(value) {
      return value.length > 1;
    },
  },
  // data() {
  //   return {
  //     open: false,
  //     active: 'first',
  //     first: false,
  //     second: false,
  //     third: false,
  //     value: null,
  //     portfolioName: '',
  //     info: '',
  //     secondStepError: null,
  //     firstStepError: null,
  //     msg: {
  //       portfolioName: false,
  //     },
  //   };
  // },
  watch: {
    portfolioName: {
      handler: function portfolioName(value) {
        this.portfolioName = value;
        this.valid = this.validName(value);
      },
    },
  },
  // methods: {
  //   validName(value) {
  //     return value.length > 1;
  //   },
  //   setDone(id, index) {
  //     if (this[id] === 'first') {
  //       if (this.portfolioName === '') {
  //         this.msg.portfolioName = '';
  //       }
  //     }
  //     this[id] = true;
  //     if (index) {
  //       this.active = index;
  //     }
  //     if (this.third) {
  //       // here dispatch portfolio creation
  //     }
  //     this.secondStepError = null;
  //   },
  //   setError() {
  //     this.secondStepError = 'This is an error!';
  //   },
  //   onConfirm() {
  //     this.setDone('third');
  //     this.open = false;
  //   },
  // },
};
</script>
<style scoped>
.md-icon {
  position: absolute;
  right: 4%;
}
</style>
