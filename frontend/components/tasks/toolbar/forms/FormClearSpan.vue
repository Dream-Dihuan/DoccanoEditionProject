<template>
  <v-form>
    <v-card-text>
      <p>{{ $t('labels.clearSpanMessage') }}</p>
      <v-select
        v-model="selectedLabel"
        :items="spanLabels"
        item-text="text"
        item-value="id"
        :label="$t('labels.selectSpanType')"
        outlined
        dense
      >
        <template #selection="{ item }">
          <v-chip
            :color="item.backgroundColor"
            :text-color="$contrastColor(item.backgroundColor)"
            small
          >
            <v-avatar v-if="item.suffixKey" left color="white" class="black--text font-weight-bold">
              {{ item.suffixKey }}
            </v-avatar>
            {{ item.text }}
          </v-chip>
        </template>
        <template #item="{ item }">
          <v-chip
            :color="item.backgroundColor"
            :text-color="$contrastColor(item.backgroundColor)"
            small
          >
            <v-avatar v-if="item.suffixKey" left color="white" class="black--text font-weight-bold">
              {{ item.suffixKey }}
            </v-avatar>
            {{ item.text }}
          </v-chip>
        </template>
      </v-select>
    </v-card-text>

    <v-card-actions>
      <v-spacer />
      <v-btn text @click="$emit('click:cancel')">
        {{ $t('generic.cancel') }}
      </v-btn>
      <v-btn
        color="primary"
        text
        :disabled="!selectedLabel"
        @click="$emit('click:ok', selectedLabel)"
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
    },
    spanTypes: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  data() {
    return {
      selectedLabel: null
    }
  },

  computed: {
    spanLabels(): any[] {
      // 获取所有在spans中实际使用的span类型
      const usedLabelIds = [...new Set(this.spans.map((span: any) => span.label))]
      return this.spanTypes.filter((type: any) => usedLabelIds.includes(type.id))
    }
  }
})
</script>