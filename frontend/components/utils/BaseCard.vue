<template>
  <v-card class="base-card shadow-soft" flat>
    <v-toolbar color="transparent" flat class="base-card__toolbar">
      <v-toolbar-title class="base-card__title">{{ title }}</v-toolbar-title>
    </v-toolbar>
    <v-divider />
    <v-card-text class="base-card__content">
      <slot name="content" />
    </v-card-text>
    <v-card-actions class="base-card__actions">
      <v-spacer />
      <v-btn
        v-if="cancelText"
        class="text-capitalize base-card__btn base-card__btn--ghost"
        text
        color="primary"
        data-test="cancel-button"
        @click="cancel"
      >
        {{ cancelText }}
      </v-btn>
      <v-btn
        v-if="agreeText"
        :disabled="disabled"
        class="text-none base-card__btn base-card__btn--primary"
        text
        data-test="delete-button"
        @click="agree"
      >
        {{ agreeText }}
      </v-btn>
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import Vue from 'vue'
export default Vue.extend({
  props: {
    title: {
      type: String,
      default: '',
      required: true
    },
    cancelText: {
      type: String,
      default: ''
    },
    agreeText: {
      type: String,
      default: ''
    },
    disabled: {
      type: Boolean,
      default: false
    }
  },

  methods: {
    agree() {
      this.$emit('agree')
    },
    cancel() {
      this.$emit('cancel')
    }
  }
})
</script>

<style scoped>
@import '@/assets/style/theme.css';

.base-card {
  border-radius: 12px;
  background: var(--card-bg);
  border: 2px solid var(--card-border);
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
}

.base-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.1);
}

.theme--dark .base-card {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
  border: 2px solid var(--card-border);
}

.theme--dark .base-card:hover {
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.3);
}

.base-card__toolbar {
  padding: 16px 24px;
}

.base-card__title {
  font-weight: 700;
  color: var(--text-primary);
  font-size: 18px;
  letter-spacing: 0.1px;
}

.v-divider {
  background-color: var(--card-border) !important;
}

.base-card__content {
  padding: 24px;
  color: var(--text-secondary);
}

.base-card__actions {
  padding: 16px 24px;
}

.base-card__btn {
  border-radius: 8px;
  font-weight: 600;
  min-width: 100px;
  height: 40px;
  box-shadow: none !important;
  text-transform: none !important;
}

.base-card__btn--ghost {
  color: var(--primary);
  background: transparent;
  border: 1px solid var(--primary);
}

.base-card__btn--ghost:hover {
  background: var(--primary-light);
}

.theme--dark .base-card__btn--ghost {
  background: transparent;
}

.theme--dark .base-card__btn--ghost:hover {
  background: rgba(25, 118, 210, 0.2);
}

.base-card__btn--primary {
  background: var(--primary);
  color: white !important;
  border: 1px solid var(--primary);
}

.base-card__btn--primary:hover {
  background: var(--primary-dark);
  border-color: var(--primary-dark);
}

.base-card__btn--primary:disabled {
  background: var(--primary-light);
  border-color: var(--primary-light);
  opacity: 0.7;
}
</style>