<template>
  <v-container class="py-16">
    <v-row justify="center" class="mb-12">
      <v-col cols="12" class="text-center">
        <h2 class="display-2 font-weight-bold mb-4">
          {{ $t('home.featuresTitle') }}
        </h2>
        <v-divider class="mx-auto" style="max-width: 100px;"></v-divider>
      </v-col>
    </v-row>
    
    <v-row justify="center">
      <v-col v-for="(item, index) in featureCards" :key="index" cols="12" sm="6" md="4" class="d-flex">
        <v-card class="flex-grow-1 pa-6 feature-card" elevation="4" height="100%">
          <v-row justify="center" class="my-4">
            <v-icon size="64" color="primary">{{ getFeatureIcon(index) }}</v-icon>
          </v-row>
          <v-card-title class="justify-center px-0">
            <h3 class="headline text-center font-weight-bold mb-2">
              {{ item.title }}
            </h3>
          </v-card-title>
          <v-card-text class="text-center px-0">
            <p class="subtitle-1 mb-0">
              {{ item.text }}
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiAccountGroup, mdiWeb, mdiOpenSourceInitiative } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      featureCards: [
        {
          title: this.$t('home.featuresTitle1'),
          text: this.$t('home.featuresText1')
        },
        {
          title: this.$t('home.featuresTitle2'),
          text: this.$t('home.featuresText2')
        },
        {
          title: this.$t('home.featuresTitle3'),
          text: this.$t('home.featuresText3')
        }
      ],
      icons: [mdiAccountGroup, mdiWeb, mdiOpenSourceInitiative]
    }
  },
  
  methods: {
    getFeatureIcon(index: number) {
      return this.icons[index];
    }
  }
})
</script>

<style scoped>
.feature-card {
  transition: all 0.3s ease-in-out;
  border-radius: 12px;
}

.feature-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.15) !important;
}
</style>