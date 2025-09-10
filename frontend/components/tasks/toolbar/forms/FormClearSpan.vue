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
            v-bind="attrs"
            :input-value="selected"
            :color="item.backgroundColor"
            :text-color="$contrastColor(item.backgroundColor)"
            small
            style="white-space: normal; height: auto;"
          >
            <!-- <v-avatar 
              v-if="item.suffixKey" 
              left 
              color="white" 
              class="black--text font-weight-bold" 
              style="width: auto; min-width: 24px; padding: 0 6px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;"
            >
              <span style="font-size: 0.75rem;">{{ item.suffixKey }}</span>
            </v-avatar> -->
            <span style="white-space: normal; word-break: break-word; margin-left: 4px;">{{ item.text }}</span>
          </v-chip>
        </template>
        <template #item="{ item }">
          <v-list-item-content>
            <v-chip 
              :color="item.backgroundColor" 
              :text-color="$contrastColor(item.backgroundColor)" 
              small
              style="white-space: normal; height: auto; max-width: 100%;"
            >
              <!-- <v-avatar 
                v-if="item.suffixKey" 
                left 
                color="white" 
                class="black--text font-weight-bold" 
                style="width: auto; min-width: 24px; padding: 0 6px; display: inline-flex; align-items: center; justify-content: center; flex-shrink: 0;"
              >
                <span style="font-size: 0.75rem;">{{ item.suffixKey }}</span>
              </v-avatar> -->
              <span style="white-space: normal; word-break: break-word; margin-left: 4px;">{{ item.text }}</span>
            </v-chip>
          </v-list-item-content>
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