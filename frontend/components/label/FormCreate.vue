<template>
  <v-card dense>
    <v-card-title class="subtitle-1">{{ $t('labels.createLabelType') }}</v-card-title>
    <v-card-text class="pa-2">
      <v-form ref="form" v-model="valid">
        <v-row dense>
          <v-col cols="12" sm="6">
            <v-text-field
              :value="source"
              :counter="999"
              :label="$t('labels.source')"
              outlined
              required
              dense
              @input="$emit('update:source', $event)"
            />
          </v-col>
          <v-col v-if="source !== undefined" cols="12" sm="6">

           <v-text-field
              :value="text"
              :counter="9000"
              :label="$t('labels.labelName')"
              :rules="[rules.required, rules.counter, rules.nameDuplicated]"
              outlined
              required
              dense
              @input="$emit('update:text', $event)"
            />
          </v-col>
          <v-col v-if="type !== 'category'" cols="24" sm="12">
            <div class="d-flex align-center" style="width: 100%;">
              <v-text-field
                :value="suffixKey"
                :counter="10"
                :label="$t('labels.key')"
                :rules="[rules.keyCounter]"
                ref="suffixKeyField"
                outlined
                dense
                style="width: 90%;"
                @input="$emit('update:suffixKey', $event)"
              />
              <v-btn
                ref="booleanButton"
                class="ml-2"
                small
                @click="fillSuffixKeyWithBoolean"
              >
                {{ $t('labels.booleanValue') }}
              </v-btn>
            </div>
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="12" sm="12" class="py-1">
            <v-text-field
              :value="backgroundColor"
              :rules="[rules.validColor]"
              :label="$t('labels.color')"
              hide-details="auto"
              outlined
              required
              dense
              @input="$emit('update:backgroundColor', $event)"
            />
            <v-chip-group v-model="selectedColorIndex" column mandatory @change="onColorSelect">
              <v-chip
                v-for="color in predefinedColors"
                :key="color"
                :color="color"
                filter
                label
                class="ma-1"
                small
                style="height: 24px; width: 24px"
              />
              <v-tooltip bottom>
                <template #activator="{ on, attrs }">
                  <v-chip 
                    label 
                    class="ma-1" 
                    small
                    v-bind="attrs" 
                    v-on="on" 
                    @click="setRandomColor"
                  >
                    <v-icon x-small>{{ mdiReload }}</v-icon>
                    {{ $t('labels.randomColor') }}
                  </v-chip>
                </template>
                <span>{{ $t('labels.randomColorTooltip') }}</span>
              </v-tooltip>
            </v-chip-group>
          </v-col>
        </v-row>

        <v-row>
          <v-col>
            <div class="subtitle-2 black--text mb-1">{{ $t('labels.preview') }}</div>
            <v-chip :color="backgroundColor" :text-color="textColor" small>
              {{ source +" - "+text }}
              <!-- <v-avatar v-if="suffixKey" right color="white" class="black--text font-weight-bold">
                {{ suffixKey }}
                
              </v-avatar> -->
            </v-chip>
          </v-col>
        </v-row>

        <v-row>
          <v-col cols="12" sm="12">
            <slot :valid="valid" />
          </v-col>
        </v-row>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script lang="ts">
import { mdiReload } from '@mdi/js'
import type { PropType } from 'vue'
import Vue from 'vue'
import { LabelDTO } from '~/services/application/label/labelData'

export default Vue.extend({
  props: {
    items: {
      type: Array as PropType<LabelDTO[]>,
      default: () => [],
      required: true
    },
    id: {
      type: Number as () => number | undefined,
      default: undefined
    },
    text: {
      type: String,
      default: ''
    },
    source: {
      type: String,
      default: undefined
    },
    prefixKey: {
      type: String as PropType<string | null>,
      default: null
    },
    suffixKey: {
      type: String as PropType<string | null>,
      default: null
    },
    backgroundColor: {
      type: String,
      default: '#73D8FF'
    },
    textColor: {
      type: String,
      default: '#ffffff'
    },
    type: {
      type: String,
      default: 'span' // 默认为span类型，这样不会影响现有功能
    }
  },

  data() {
    return {
      valid: false,
      selectedColorIndex: -1,
      mdiReload,
      predefinedColors: [
        '#73D8FF',
        '#FF9E80',
        '#A0D888',
        '#FFD700',
        '#BA68C8',
        '#FF6B6B',
        '#6EC1E4',
        '#FFB347',
        '#98FB98',
        '#DDA0DD'
      ],
      availableSuffixKeys: [
        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j',
        'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
        'u', 'v', 'w', 'x', 'y', 'z'
      ],
      rules: {
        required: (value: string) => !!value || this.$t('rules.requiredRules'),
        counter: (value: string) => value.length <= 9999 || this.$t('rules.counterRules'),
        keyCounter: (value: string) => !value || value.length <= 10 || this.$t('rules.keyCounterRules'),
        nameDuplicated: (value: string) => {
          const isDuplicated = this.items.some((item) => item.text === value && item.id !== this.id)
          return !isDuplicated || this.$t('rules.nameDuplicatedRules')
        },
        validColor: (value: string) => {
          const isHex = /^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$/.test(value)
          return isHex || this.$t('rules.validColorRules')
        }
      }
    }
  },

  methods: {
    setRandomColor() {
      const randomIndex = Math.floor(Math.random() * this.predefinedColors.length)
      this.selectedColorIndex = randomIndex
      this.$emit('update:backgroundColor', this.predefinedColors[randomIndex])
    },
    
    onColorSelect(index: number) {
      if (index !== -1) {
        this.$emit('update:backgroundColor', this.predefinedColors[index])
      }
    },

    fillSuffixKeyWithBoolean() {
      this.$emit('update:suffixKey', this.$t('labels.booleanValue'))
    },

    isBooleanValue() {
      return this.suffixKey === this.$t('labels.booleanValue')
    }
  }
})
</script>