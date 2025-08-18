<template>
  <v-app id="inspire">
    <v-main>
      <v-container 
        class="fill-height d-flex align-center justify-center" 
        fluid
        :class="{'dark-mode-bg': $vuetify.theme.dark}"
        style="min-height: 100vh"
      >
        <div class="d-flex flex-column align-center">
          <div class="text-center mb-8">
            <h1 class="text-h3 font-weight-bold primary--text">
              {{ $t('home.mainTitle') }}
            </h1>
            <p class="text-h6 grey--text mt-2">
              {{ $t('home.subtitle') }}
            </p>
          </div>
          
          <v-col cols="12" sm="10" md="8" lg="6" xl="5">
            <form-login :login="authenticateUser" />
            <social-login :fetch-social-link="fetchSocialLink" />
          </v-col>
          
          <div class="mt-8 text-center caption grey--text">
            &copy; {{ new Date().getFullYear() }} {{ $t('home.mainTitle') }}
          </div>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>

<script lang="ts">
import Vue from 'vue'
import { mapActions } from 'vuex'
import FormLogin from '@/components/auth/FormLogin.vue'
import SocialLogin from '@/components/auth/SocialLogin.vue'

export default Vue.extend({
  components: {
    FormLogin,
    SocialLogin
  },

  methods: {
    ...mapActions('auth', ['authenticateUser', 'fetchSocialLink'])
  },
  
  metaInfo() {
    return {
      title: this.$t('user.login') as string
    }
  }
})
</script>

<style scoped>
.v-container {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%) !important;
}

.v-container.dark-mode-bg {
  background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%) !important;
}

@media (min-width: 1904px) {
  :deep(.v-col) {
    max-width: 500px;
  }
}

@media (min-width: 2500px) {
  :deep(.v-col) {
    max-width: 600px;
  }
}
</style>