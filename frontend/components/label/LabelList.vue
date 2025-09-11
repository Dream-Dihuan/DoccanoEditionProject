<template>
  <div class="label-list-wrapper">
    <v-data-table
      :value="value"
      :headers="headers"
      :items="sortedItems"
      :search="search"
      :loading="isLoading"
      :loading-text="$t('generic.loading')"
      :no-data-text="$t('vuetify.noDataAvailable')"
      :footer-props="{
        showFirstLastPage: true,
        'items-per-page-text': $t('vuetify.itemsPerPageText'),
        'page-text': $t('dataset.pageText')
      }"
      item-key="id"
      show-select
      @input="$emit('input', $event)"
    >
      <template #top>
        <v-text-field
          v-model="search"
          :prepend-inner-icon="mdiMagnify"
          :label="$t('generic.search')"
          single-line
          hide-details
          filled
          rounded
          dense
          class="mb-4"
        />
      </template>
      <template #[`item.backgroundColor`]="props">
        <v-chip
          :color="props.item.backgroundColor"
          :text-color="$contrastColor(props.item.backgroundColor)"
          small
        >
          {{ props.item.backgroundColor }}
        </v-chip>
      </template>
      <template #[`item.actions`]="{ item }">
        <v-tooltip bottom>
          <template #activator="{ on, attrs }">
            <v-btn
              icon
              small
              v-bind="attrs"
              v-on="on"
              @click="$emit('toggle-favorite', item)"
            >
              <v-icon :color="isFavorite(item) ? 'yellow' : 'grey'">
                {{ isFavorite(item) ? mdiStar : mdiStarOutline }}
              </v-icon>
            </v-btn>
          </template>
          <span>{{ isFavorite(item) ? '取消置顶' : '置顶标签' }}</span>
        </v-tooltip>
        <v-icon 
          v-if="!disableEdit"
          small 
          @click="$emit('edit', item)"
        >
          {{ mdiPencil }}
        </v-icon>
      </template>
    </v-data-table>
  </div>
</template>

<script lang="ts">
import { mdiMagnify, mdiPencil, mdiStar, mdiStarOutline } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  props: {
    isLoading: {
      type: Boolean,
      default: false,
      required: true
    },
    items: {
      type: Array as PropType<LabelDTO[]>,
      default: () => [],
      required: true
    },
    value: {
      type: Array as PropType<LabelDTO[]>,
      default: () => [],
      required: true
    },
    disableEdit: {
      type: Boolean,
      default: false
    },
    favoriteLabels: {
      type: Array as PropType<number[]>,
      default: () => [],
      required: false
    }
  },

  data() {
    return {
      search: '',
      mdiPencil,
      mdiMagnify,
      mdiStar,
      mdiStarOutline
    }
  },

  computed: {
    headers() {
      const headers = [
        { text: this.$t('generic.name'), value: 'text', sortable: true },
        { text: this.$t('labels.shortkey'), value: 'suffixKey', sortable: true },
        { text: this.$t('labels.color'), value: 'backgroundColor', sortable: true }
      ]
      if (!this.disableEdit) {
        headers.push({ text: this.$t('generic.actions'), value: 'actions', sortable: false })
      }
      return headers
    },

    sortedItems(): LabelDTO[] {
      // 将置顶标签排在前面
      return [...this.items].sort((a, b) => {
        const aIsFavorite = this.isFavorite(a) ? 1 : 0
        const bIsFavorite = this.isFavorite(b) ? 1 : 0
        return bIsFavorite - aIsFavorite
      })
    }
  },

  methods: {
    isFavorite(item: LabelDTO): boolean {
      return this.favoriteLabels.includes(item.id)
    }
  }
})
</script>

<style scoped>
.label-list-wrapper ::v-deep .v-data-table {
  background-color: transparent;
}

.label-list-wrapper ::v-deep .v-data-table-header {
  background-color: var(--background);
}

.label-list-wrapper ::v-deep .v-data-table tbody tr:hover:not(.v-data-table__selected) {
  background-color: var(--background) !important;
}
</style>