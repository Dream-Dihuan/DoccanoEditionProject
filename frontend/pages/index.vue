<template>
  <v-main>
    <the-top-banner />
    <feature-cards />
    <v-container class="py-16">
      <v-row justify="center">
        <v-col cols="12" md="8" class="text-center">
          <h2 class="display-1 font-weight-bold mb-6">{{ $t('home.trustedBy') }}</h2>
          <p class="headline mb-10">
            {{ $t('home.trustedByDescription') }}
          </p>
          <v-btn x-large color="primary" class="white--text" :href="localePath('/auth')">
            {{ $t('home.getStartedToday') }}
          </v-btn>
        </v-col>
      </v-row>
    </v-container>
    <the-bottom-banner />
  </v-main>
</template>

<script>
import FeatureCards from '@/components/layout/FeatureCards'
import TheTopBanner from '@/components/layout/TheTopBanner'
import TheBottomBanner from '@/components/layout/TheBottomBanner'

export default {
  components: {
    FeatureCards,
    TheTopBanner,
    TheBottomBanner
  }
}
</script>