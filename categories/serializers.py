from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from .models import Category


class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = (
            "id",
            "name",
        )


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(
        max_length=256, validators=[UniqueValidator(queryset=Category.objects.all())]
    )
    parents = CategoryItemSerializer(many=True, required=False, read_only=True)
    children = CategoryItemSerializer(many=True, required=False, read_only=True)
    siblings = CategoryItemSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Category
        fields = ("id", "name", "parents", "children", "siblings")

    def create(self, validated_data):
        return Category.objects.create(
            name=validated_data["name"], parent=self.context["parent"]
        )


class CategoryCreateSerializer(serializers.Serializer):
    body = serializers.JSONField(required=True)

    def save(self):
        def create_category(category_data: dict, parent: Category = None):
            serializer = CategorySerializer(
                data=category_data, context={"parent": parent}
            )
            serializer.is_valid(raise_exception=True)
            category = serializer.save()
            for child_data in category_data.get("children", ()):
                create_category(child_data, category)

        create_category(self.validated_data["body"])
