from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import CategoryType, LabelType, RelationType, SpanType


class LabelSerializer(serializers.ModelSerializer):
    def validate(self, attrs):
        prefix_key = attrs.get("prefix_key")
        suffix_key = attrs.get("suffix_key")

        # In the case of user don't set any shortcut key.
        if prefix_key is None and suffix_key is None:
            return super().validate(attrs)

        # Don't allow shortcut key not to have a suffix key.
        if prefix_key and not suffix_key:
            raise ValidationError("Shortcut key may not have a suffix key.")

        # Allow duplicate shortcut keys - removed the validation that was preventing duplicates
        return super().validate(attrs)

    class Meta:
        model = LabelType
        fields = (
            "id",
            "text",
            "prefix_key",
            "suffix_key",
            "background_color",
            "text_color",
        )


class CategoryTypeSerializer(LabelSerializer):
    class Meta:
        model = CategoryType
        fields = LabelSerializer.Meta.fields


class SpanTypeSerializer(LabelSerializer):
    class Meta:
        model = SpanType
        fields = LabelSerializer.Meta.fields


class RelationTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = RelationType
        fields = LabelSerializer.Meta.fields