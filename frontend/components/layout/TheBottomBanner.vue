<template>
  <section class="bottom-banner">
    <v-container class="py-16">
      <v-row justify="center" align="center">
        <v-col cols="12" class="text-center mb-10">
          <h2 class="display-2 font-weight-bold mb-4">
            {{ $t('home.footerTitle') }}
          </h2>
          <p class="headline mx-auto" style="max-width: 700px;">
            {{ $t('home.footerSubtitle') }}
          </p>
        </v-col>
      </v-row>
      
      <v-row justify="center">
        <v-col cols="12" md="10">
          <v-sheet rounded="lg" elevation="8" class="pa-8 pa-md-12">
            <v-row align="center">
              <v-col cols="12" md="6" class="text-center text-md-right mb-6 mb-md-0">
                <v-img 
                  :src="require(`~/assets/ner_demo.png`)" 
                  max-height="300" 
                  contain 
                  class="mx-auto" 
                  alt="Demo Preview"
                />
              </v-col>
              <v-col cols="12" md="6" class="text-center text-md-left">
                <h3 class="display-1 font-weight-bold mb-6">
                  {{ $t('home.experienceIt') || 'Experience It Firsthand' }}
                </h3>
                <p class="subtitle-1 mb-8">
                  {{ $t('home.experienceDescription') || 'Try our live demos to see how doccano can accelerate your annotation workflow.' }}
                </p>
                <v-menu open-on-hover offset-y nudge-bottom="10">
                  <template #activator="{ on, attrs }">
                    <v-btn x-large color="primary" class="white--text px-8" v-bind="attrs" v-on="on">
                      {{ $t('home.demoDropDown') }}
                      <v-icon right dark>
                        {{ mdiMenuDown }}
                      </v-icon>
                    </v-btn>
                  </template>
                  <v-list>
                    <v-list-item
                      v-for="(item, index) in items"
                      :key="index"
                      @click="$router.push(localePath('/demo/' + item.link))"
                    >
                      <v-list-item-title>{{ item.title }}</v-list-item-title>
                    </v-list-item>
                  </v-list>
                </v-menu>
              </v-col>
            </v-row>
          </v-sheet>
        </v-col>
      </v-row>
    </v-container>
  </section>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiMenuDown } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      items: [
        { title: this.$t('home.demoNER'), link: 'named-entity-recognition' },
        { title: this.$t('home.demoSent'), link: 'sentiment-analysis' },
        { title: this.$t('home.demoTranslation'), link: 'translation' },
        { title: this.$t('home.demoTextToSQL'), link: 'text-to-sql' }
      ],
      mdiMenuDown
    }
  }
})
</script>

<style scoped>
.bottom-banner {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4edf5 100%);
}

/* Dark theme override */
.theme--dark .bottom-banner {
  background: linear-gradient(135deg, #1E1E2C 0%, #2D2D44 100%);
}

.theme--dark .bottom-banner .v-sheet {
  background: #1E1E2C !important;
  color: white;
}
</style>