from rest_framework import serializers


class AggregatedTransactionSerializer(serializers.Serializer):
    key = serializers.CharField()
    value = serializers.IntegerField()
