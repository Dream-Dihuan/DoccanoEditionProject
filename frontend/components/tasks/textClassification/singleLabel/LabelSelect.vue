<template>
  <v-select
    :value="annotatedLabel"
    chips
    :items="labels"
    item-text="text"
    hide-details
    hide-selected
    return-object
    class="pt-0"
    @change="addOrRemove"
  >
    <template #selection="{ attrs, item, select, selected }">
      <v-chip
        v-if="item.backgroundColor"
        v-bind="attrs"
        :input-value="selected"
        :color="item.backgroundColor"
        :text-color="$contrastColor(item.backgroundColor)"
        close
        @click="select"
        @click:close="remove(item)"
        style="white-space: normal; height: auto;"
      >
        <v-avatar v-if="item.suffixKey" left color="white" class="black--text font-weight-bold">
          {{ item.suffixKey }}
        </v-avatar>
        <span style="white-space: normal; word-break: break-word;">{{ item.text }}</span>
      </v-chip>
    </template>
    <template #item="{ item }">
      <v-list-item-content>
        <v-chip 
          :color="item.backgroundColor" 
          :text-color="$contrastColor(item.backgroundColor)" 
          style="white-space: normal; height: auto; max-width: 100%;"
        >
          <v-avatar v-if="item.suffixKey" left color="white" class="black--text font-weight-bold">
            {{ item.suffixKey }}
          </v-avatar>
          <span style="white-space: normal; word-break: break-word;">{{ item.text }}</span>
        </v-chip>
      </v-list-item-content>
    </template>
  </v-select>
</template>

<script>
export default {
  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    annotations: {
      type: Array,
      default: () => [],
      required: true
    }
  },

  computed: {
    annotatedLabel() {
      const labelIds = this.annotations.map((item) => item.label)
      return this.labels.find((item) => labelIds.includes(item.id))
    }
  },

  methods: {
    addOrRemove(val) {
      if (val) {
        this.add(val)
      } else {
        this.remove(this.annotatedLabel)
      }
    },

    add(label) {
      this.$emit('add', label.id)
    },

    remove(label) {
      const annotation = this.annotations.find((item) => item.label === label.id)
      this.$emit('remove', annotation.id)
    }
  }
}
</script>