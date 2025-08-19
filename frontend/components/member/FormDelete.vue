<template>
  <div>
    <v-card-text class="pt-5">
      <p>{{ $t('members.removePrompt') }}</p>
      <v-list v-if="selected.length > 0">
        <v-list-item v-for="(selItem, i) in selected.slice(0, 10)" :key="i">
          <v-list-item-content>
            <v-list-item-title>{{ selItem.username }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
        <v-list-item v-if="selected.length > 10">
          <v-list-item-content>
            <v-list-item-title>... and {{ selected.length - 10 }} more</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>
    <v-card-actions>
      <v-spacer></v-spacer>
      <v-btn text @click="$emit('cancel')">
        {{ $t('generic.cancel') }}
      </v-btn>
      <v-btn color="primary" @click="$emit('remove')">
        {{ $t('generic.yes') }}
      </v-btn>
    </v-card-actions>
  </div>
</template>

<script lang="ts">
import Vue from 'vue'

export default Vue.extend({
  props: {
    selected: {
      type: Array,
      default: () => []
    }
  }
})
</script>