<template>
  <v-card v-if="social.length > 0" class="elevation-2 rounded-lg mt-6" :outlined="$vuetify.theme.dark">
    <v-card-text class="py-4">
      <div class="d-flex align-center">
        <v-divider></v-divider>
        <span class="px-4 text--secondary caption text-uppercase">{{ $t('home.experienceIt') }}</span>
        <v-divider></v-divider>
      </div>
      
      <div class="mt-4">
        <v-btn
          v-for="item in social"
          :key="item.provider"
          block
          :elevation="$vuetify.theme.dark ? 0 : 1"
          color="secondary"
          :href="item.href"
          class="mt-3 text-capitalize"
          :outlined="$vuetify.theme.dark"
          :class="{'white--text': !$vuetify.theme.dark, 'accent--text': $vuetify.theme.dark}"
        >
          {{ $t('user.socialLogin', { provider: item.provider }) }}
        </v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import type { PropType } from 'vue'
import Vue from 'vue'

export default Vue.extend({
  props: {
    fetchSocialLink: {
      type: Function as PropType<() => Promise<any>>,
      required: true
    }
  },
  data() {
    return {
      social: [] as any[]
    }
  },
  async mounted() {
    try {
      const response = await this.fetchSocialLink()
      this.social = Object.entries(response)
        .map(([key, value]: any) => ({
          provider: key,
          value
        }))
        .filter((item) => !!item.value?.authorize_url)
        .map((item: any) => ({
          ...item,
          href: `${item.value.authorize_url}&redirect_uri=${location.origin}${item.value.redirect_path}`
        }))
    } catch (e) {
      console.error(e)
    }
  }
})
</script>

<style scoped>
.v-card {
  border-radius: 12px !important;
}
</style>