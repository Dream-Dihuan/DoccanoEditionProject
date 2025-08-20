<template>
  <base-card :cancel-text="$t('generic.close')" @cancel="close">
    <template #content>
      <v-simple-table>
        <template #default>
          <thead>
            <tr>
              <th class="text-left">{{ $t('annotation.action') }}</th>
              <th class="text-left">{{ $t('annotation.key') }}</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="item in items" :key="item.name">
              <td>{{ item.name }}</td>
              <td>
                <v-chip
                  v-for="key in item.key"
                  :key="key"
                  color="grey darken-3 white--text"
                  class="ma-1"
                  label
                  small
                  >{{ key }}</v-chip
                >
              </td>
            </tr>
          </tbody>
        </template>
      </v-simple-table>
    </template>
  </base-card>
</template>

<script>
import BaseCard from '@/components/utils/BaseCard'

export default {
  components: {
    BaseCard
  },

  data() {
    return {
      items: [
        {
          name: this.$t('annotation.jumpToFirstData'),
          key: ['shift', '←']
        },
        {
          name: this.$t('annotation.jumpToLastData'),
          key: ['shift', '→']
        },
        {
          name: this.$t('annotation.moveToPreviousData'),
          key: ['←']
        },
        {
          name: this.$t('annotation.moveToNextData'),
          key: ['→']
        },
        {
          name: this.$t('annotation.confirmData'),
          key: ['enter']
        }
      ]
    }
  },

  methods: {
    close() {
      this.$emit('click:close')
    }
  }
}
</script>