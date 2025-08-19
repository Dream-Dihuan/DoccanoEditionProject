<template>
  <v-card class="elevation-12 rounded-lg" :loading="loading">
    <v-toolbar color="primary" dark flat class="rounded-t-lg" :class="{'darken-2': $vuetify.theme.dark}">
      <v-toolbar-title class="text-h6">{{ $t('user.login') }}</v-toolbar-title>
      <v-spacer></v-spacer>
    </v-toolbar>
    
    <v-card-text class="mt-5">
      <v-form ref="form" v-model="valid">
        <v-alert v-show="showError" v-model="showError" type="error" dismissible outlined>
          {{ errorMessage }}
        </v-alert>
        
        <v-text-field
          v-model="username"
          :rules="userNameRules"
          :label="$t('user.username')"
          name="username"
          :prepend-icon="mdiAccount"
          type="text"
          autofocus
          outlined
          dense
          @keyup.enter="tryLogin"
        />
        
        <v-text-field
          id="password"
          v-model="password"
          :rules="passwordRules"
          :label="$t('user.password')"
          name="password"
          :prepend-icon="mdiLock"
          type="password"
          outlined
          dense
          class="mt-4"
          @keyup.enter="tryLogin"
        />
      </v-form>
    </v-card-text>
    
    <v-card-actions class="px-6 pb-6">
      <v-btn
        :disabled="!valid || loading"
        color="primary"
        block
        large
        depressed
        :class="{'white--text': !$vuetify.theme.dark, 'text--primary': $vuetify.theme.dark}"
        @click="tryLogin"
      >
        {{ $t('user.login') }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiAccount, mdiLock } from '@mdi/js'

export default Vue.extend({
  props: {
    login: {
      type: Function,
      required: true
    }
  },
  
  data() {
    return {
      valid: false,
      username: '',
      password: '',
      showError: false,
      errorMessage: '',
      mdiAccount,
      mdiLock,
      loading: false,
      userNameRules: [] as Array<(v: string) => true | string>,
      passwordRules: [] as Array<(v: string) => true | string>
    }
  },

  mounted() {
    // 初始化验证规则
    this.userNameRules = [
      (v: string) => !!v || this.$t('rules.userNameRules.userNameRequired') as string,
      (v: string) => (v && v.length <= 30) || this.$t('rules.userNameRules.userNameLessThan30Chars') as string
    ];
    
    this.passwordRules = [
      (v: string) => !!v || this.$t('rules.passwordRules.passwordRequired') as string,
      (v: string) => (v && v.length <= 30) || this.$t('rules.passwordRules.passwordLessThan30Chars') as string
    ];
  },

  methods: {
    async tryLogin() {
      if (!this.valid) return
      
      this.loading = true
      this.showError = false
      this.errorMessage = ''
      try {
        await this.login({
          username: this.username,
          password: this.password
        })
        this.$router.push(this.localePath('/projects'))
      } catch (error) {
        this.showError = true
        // 使用正确的国际化键errors.invalidUserOrPass而不是projects.errors.invalidUserOrPass
        try {
          const translatedMessage = this.$t('errors.invalidUserOrPass')
          this.errorMessage = typeof translatedMessage === 'string' 
            ? translatedMessage 
            : '用户名或密码不正确，或出现了其他问题'
        } catch (translationError) {
          // 如果国际化函数出错，使用默认中文文本
          this.errorMessage = '用户名或密码不正确，或出现了其他问题'
        }
      } finally {
        this.loading = false
      }
    }
  }
})
</script>

<style scoped>
.v-card {
  border-radius: 12px !important;
}

.v-toolbar {
  border-radius: 8px 8px 0 0 !important;
}

:deep(.v-text-field) {
  padding-top: 4px;
  padding-bottom: 4px;
}
</style>