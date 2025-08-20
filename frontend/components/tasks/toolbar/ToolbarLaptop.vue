<template>
  <v-toolbar class="toolbar-control" dense flat>
    <v-row no-gutters>
      <v-btn-toggle>
        <button-review :is-reviewd="isReviewd" @click:review="$emit('click:review')" />

        <button-filter :value="filterOption" @click:filter="changeFilter" />

        <button-order :value="orderOption" @click:order="changeOrder" />

        <button-guideline @click:guideline="dialogGuideline = true" />
        <v-dialog v-model="dialogGuideline" max-width="800">
          <v-card>
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title class="white--text">
                {{ $t('annotation.guidelinePopupTitle') }}
              </v-toolbar-title>
            </v-toolbar>
            <form-guideline :guideline-text="guidelineText" @click:close="dialogGuideline = false" />
          </v-card>
        </v-dialog>

        <button-comment @click:comment="dialogComment = true" />
        <v-dialog v-model="dialogComment" max-width="800">
          <v-card>
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title class="white--text">
                {{ $t('comments.comments') }}
              </v-toolbar-title>
            </v-toolbar>
            <form-comment :example-id="docId" @click:cancel="dialogComment = false" />
          </v-card>
        </v-dialog>

        <button-auto-labeling @click:auto="dialogAutoLabeling = true" />
        <v-dialog v-model="dialogAutoLabeling" max-width="800">
          <v-card>
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title class="white--text">
                {{ $t('generic.settings') }}
              </v-toolbar-title>
            </v-toolbar>
            <form-auto-labeling
              :is-enabled="enableAutoLabeling"
              :error-message="errorMessage"
              @click:cancel="dialogAutoLabeling = false"
              @input="updateAutoLabeling"
            />
          </v-card>
        </v-dialog>

        <button-clear @click:clear="dialogClear = true" />
        <v-dialog v-model="dialogClear" max-width="500">
          <v-card>
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title class="white--text">
                {{ $t('annotation.clearAnnotationsTitle') }}
              </v-toolbar-title>
            </v-toolbar>
            <form-clear-label
              @click:ok="
                $emit('click:clear-label')
                dialogClear = false
              "
              @click:cancel="dialogClear = false"
            />
          </v-card>
        </v-dialog>

        <button-keyboard-shortcut @click:open="dialogShortcut = true" />
        <v-dialog v-model="dialogShortcut" max-width="800">
          <v-card>
            <v-toolbar color="primary" dark flat>
              <v-toolbar-title class="white--text">
                {{ $t('generic.keyboardShortcut') }}
              </v-toolbar-title>
            </v-toolbar>
            <form-keyboard-shortcut @click:close="dialogShortcut = false" />
          </v-card>
        </v-dialog>
      </v-btn-toggle>
      <slot />
      <v-spacer />
      <button-pagination
        :value="page"
        :total="total"
        @click:prev="updatePage(page - 1)"
        @click:next="updatePage(page + 1)"
        @click:first="updatePage(1)"
        @click:last="updatePage(total)"
        @click:jump="updatePage($event)"
      />
    </v-row>
  </v-toolbar>
</template>

<script lang="ts">
import Vue from 'vue'
import ButtonAutoLabeling from './buttons/ButtonAutoLabeling.vue'
import ButtonClear from './buttons/ButtonClear.vue'
import ButtonComment from './buttons/ButtonComment.vue'
import ButtonFilter from './buttons/ButtonFilter.vue'
import ButtonGuideline from './buttons/ButtonGuideline.vue'
import ButtonOrder from './buttons/ButtonOrder.vue'
import ButtonPagination from './buttons/ButtonPagination.vue'
import ButtonReview from './buttons/ButtonReview.vue'
import ButtonKeyboardShortcut from './buttons/ButtonKeyboardShortcut.vue'
import FormAutoLabeling from './forms/FormAutoLabeling.vue'
import FormClearLabel from './forms/FormClearLabel.vue'
import FormComment from './forms/FormComment.vue'
import FormGuideline from './forms/FormGuideline.vue'
import FormKeyboardShortcut from './forms/FormKeyboardShortcut.vue'

export default Vue.extend({
  components: {
    ButtonAutoLabeling,
    ButtonClear,
    ButtonComment,
    ButtonFilter,
    ButtonGuideline,
    ButtonOrder,
    ButtonKeyboardShortcut,
    ButtonPagination,
    ButtonReview,
    FormAutoLabeling,
    FormClearLabel,
    FormComment,
    FormGuideline,
    FormKeyboardShortcut
  },

  props: {
    docId: {
      type: Number,
      required: true
    },
    enableAutoLabeling: {
      type: Boolean,
      default: false,
      required: true
    },
    guidelineText: {
      type: String,
      default: '',
      required: true
    },
    isReviewd: {
      type: Boolean,
      default: false
    },
    total: {
      type: Number,
      default: 1
    }
  },

  data() {
    return {
      dialogAutoLabeling: false,
      dialogClear: false,
      dialogComment: false,
      dialogGuideline: false,
      dialogShortcut: false,
      errorMessage: ''
    }
  },

  computed: {
    page(): number {
      // @ts-ignore
      return parseInt(this.$route.query.page, 10)
    },
    filterOption(): string {
      // @ts-ignore
      return this.$route.query.isChecked
    },
    orderOption(): string {
      // @ts-ignore
      return this.$route.query.ordering
    }
  },

  methods: {
    updatePage(page: number) {
      this.$router.push({
        query: {
          page: page.toString(),
          isChecked: this.filterOption,
          ordering: this.$route.query.ordering,
          q: this.$route.query.q
        }
      })
    },

    changeFilter(isChecked: string) {
      this.$router.push({
        query: {
          page: '1',
          isChecked,
          ordering: this.$route.query.ordering,
          q: this.$route.query.q
        }
      })
    },

    changeOrder(ordering: string) {
      this.$router.push({
        query: {
          page: '1',
          isChecked: this.filterOption,
          q: this.$route.query.q,
          ordering
        }
      })
    },

    updateAutoLabeling(isEnable: boolean) {
      if (isEnable) {
        this.$emit('update:enable-auto-labeling', true)
      } else {
        this.$emit('update:enable-auto-labeling', false)
      }
    }
  }
})
</script>

<style scoped>
.toolbar-control {
  position: sticky;
  top: 68px;
  z-index: 100;
}

.toolbar-control >>> .v-toolbar__content {
  padding: 0px !important;
}

::v-deep .v-dialog {
  width: 800px;
}
</style>
