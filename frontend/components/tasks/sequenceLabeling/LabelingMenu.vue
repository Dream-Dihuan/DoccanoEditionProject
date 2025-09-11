<template>
  <v-menu :value="opened" :position-x="x" :position-y="y" absolute offset-y @input="close">
    <v-list dense min-width="150" max-height="400" class="overflow-y-auto">
      <v-list-item>
        <v-autocomplete
          ref="autocomplete"
          v-model="value"
          :items="sortedLabels"
          autofocus
          dense
          deletable-chips
          hide-details
          item-text="text"
          item-value="id"
          label="Select a label"
          small-chips
        />
      </v-list-item>
      <v-list-item v-for="(label, i) in sortedLabels" :key="i" @click="onLabelSelected(label.id)">
        <v-list-item-action v-if="hasAnySuffixKey">
          <v-chip
            v-if="label.suffixKey"
            :color="label.backgroundColor"
            outlined
            small
            v-text="label.suffixKey"
          />
          <span v-else class="mr-8" />
        </v-list-item-action>
        <v-list-item-content>
          <v-list-item-title style="white-space: normal; word-break: break-word;">{{ label.text }}</v-list-item-title>
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-menu>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    labels: {
      type: Array,
      default: () => [],
      required: true
    },
    opened: {
      type: Boolean,
      default: false,
      required: true
    },
    selectedLabel: {
      type: Object,
      default: null,
      required: false
    },
    x: {
      type: Number,
      default: 0,
      required: true
    },
    y: {
      type: Number,
      default: 0,
      required: true
    }
  },

  data() {
    return {
      startOffset: 0,
      endOffset: 0,
      entity: null as any,
      fromEntity: null as any,
      toEntity: null as any,
      favoriteLabels: [] as number[]
    }
  },

  computed: {
    hasAnySuffixKey(): boolean {
      return this.labels.some((label: any) => label.suffixKey !== null)
    },

    value: {
      get() {
        return this.selectedLabel
      },
      set(labelId: number) {
        this.onLabelSelected(labelId)
      }
    },

    sortedLabels() {
      // 将置顶标签排在前面
      console.log('Labels:', this.labels);
      console.log('Favorite labels:', this.favoriteLabels);
      
      const sorted = [...this.labels].sort((a: any, b: any) => {
        const aIsFavorite = this.favoriteLabels.includes(a.id) ? 1 : 0;
        const bIsFavorite = this.favoriteLabels.includes(b.id) ? 1 : 0;
        // 置顶标签排在前面
        console.log(`Comparing ${a.text} (favorite: ${aIsFavorite}) with ${b.text} (favorite: ${bIsFavorite})`);
        return bIsFavorite - aIsFavorite;
      });
      
      console.log('Sorted labels:', sorted);
      return sorted;
    }
  },

  mounted() {
    // 组件挂载时加载置顶标签
    this.loadFavoriteLabels();
  },

  methods: {
    close() {
      // Todo: a bit hacky. I want to fix this problem.
      // https://github.com/vuetifyjs/vuetify/issues/10765
      this.$nextTick(() => {
        if (this.$refs.autocomplete) {
          ;(this.$refs.autocomplete as any).selectedItems = []
        }
      })
      this.$emit('close')
    },

    onLabelSelected(labelId: number) {
      this.$emit('click:label', labelId)
      this.close()
    },
    
    // 加载置顶标签
    loadFavoriteLabels() {
      // 从路由参数中获取项目ID
      const projectId = (this.$route as any)?.params?.id;
      console.log('Project ID:', projectId);
      
      if (!projectId) return;
      
      try {
        // 根据标签类型确定存储键名
        let storageKey = '';
        if (this.labels && this.labels.length > 0) {
            // 实体标签（默认）
            storageKey = `favoriteLabels_${projectId}_span`;
        }
        
        // storageKey = "favoriteLabels_4_span"
        console.log('Storage key:', storageKey);
        const saved = localStorage.getItem(storageKey);
        console.log('Saved favorite labels:', saved);
        if (saved) {
          this.favoriteLabels = JSON.parse(saved);
        }
      } catch (e) {
        console.warn('Failed to load favorite labels from localStorage', e);
        this.favoriteLabels = [];
      }
    }
  }
})
</script>