<template>
  <v-form ref="form" v-model="valid" lazy-validation>
    <v-card-text>
      <p>{{ $t('labels.clearSpanMessage') }}</p>
      <v-select
        v-model="selectedSpan"
        :items="spanItems"
        :label="$t('labels.span')"
        item-text="text"
        item-value="id"
        required
      />
    </v-card-text>
    <v-card-actions>
      <v-spacer />
      <v-btn color="blue darken-1" text @click="$emit('click:cancel')">
        {{ $t('generic.cancel') }}
      </v-btn>
      <v-btn
        :disabled="!valid || !selectedSpan"
        color="red darken-1"
        text
        @click="clearSpan"
      >
        {{ $t('generic.yes') }}
      </v-btn>
    </v-card-actions>
  </v-form>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    spans: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      valid: false,
      selectedSpan: null
    }
  },

  computed: {
    spanItems() {
      // @ts-ignore
      const uniqueSpans = [...new Map(this.spans.map(span => [span.label, span])).values()]
      // @ts-ignore
      return uniqueSpans.map(span => ({
        id: span.label,
        text: span.labelText
      }))
    }
  },

  methods: {
    clearSpan() {
      // @ts-ignore
      if (this.$refs.form.validate() && this.selectedSpan) {
        this.$emit('click:ok', this.selectedSpan)
      }
    }
  }
})
</script>