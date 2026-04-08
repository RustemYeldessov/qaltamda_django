from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category.name')
    section_name = serializers.ReadOnlyField(source='section.name')

    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ['user']