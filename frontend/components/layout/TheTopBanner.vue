<template>
  <section>
    <v-parallax :src="require(`~/assets/vbanner.jpg`)" height="600" dark>
      <v-container class="fill-height">
        <v-row class="justify-center align-center">
          <v-col cols="12" md="6" class="text-center text-md-left">
            <h1 class="display-3 font-weight-bold white--text mb-4">
              {{ $t('home.mainTitle') }}
            </h1>
            <p class="headline white--text mb-6">
              {{ $t('home.subtitle') || 'Professional text annotation tool for teams and enterprises' }}
            </p>
            <div class="d-flex flex-column flex-md-row justify-center justify-md-start">
              <v-btn x-large color="primary" class="mb-4 mb-md-0 mr-md-4 white--text" :href="localePath('/auth')">
                <v-icon left dark>
                  {{ mdiAccountArrowRight }}
                </v-icon>
                {{ $t('home.getStarted') }}
              </v-btn>
              <v-btn x-large outlined color="white" class="ml-md-4" dark href="https://github.com/doccano/doccano">
                <v-icon left>
                  {{ mdiGithub }}
                </v-icon>
                GitHub
              </v-btn>
            </div>
          </v-col>
          <v-col cols="12" md="6" class="d-none d-md-block text-center">
            <v-img :src="require('~/assets/icon.png')" alt="doccano" max-width="300" class="mx-auto" />
          </v-col>
        </v-row>
      </v-container>
    </v-parallax>
  </section>
</template>

<script lang="ts">
import Vue from 'vue'
import { mdiGithub, mdiAccountArrowRight } from '@mdi/js'

export default Vue.extend({
  data() {
    return {
      mdiGithub,
      mdiAccountArrowRight
    }
  }
})
</script>