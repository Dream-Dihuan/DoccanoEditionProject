<template>
  <v-form ref="form" v-model="valid" lazy-validation>
    <v-card-text>
      <p>{{ $t('labels.clearCategoryMessage') }}</p>
      <v-select
        v-model="selectedCategory"
        :items="categoryItems"
        :label="$t('labels.category')"
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
        :disabled="!valid || !selectedCategory"
        color="red darken-1"
        text
        @click="clearCategory"
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
    categories: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      valid: false,
      selectedCategory: null
    }
  },

  computed: {
    categoryItems() {
      // @ts-ignore
      return this.categories.map(category => ({
        id: category.id,
        text: category.text
      }))
    }
  },

  methods: {
    clearCategory() {
      // @ts-ignore
      if (this.$refs.form.validate() && this.selectedCategory) {
        this.$emit('click:ok', this.selectedCategory)
      }
    }
  }
})
</script>