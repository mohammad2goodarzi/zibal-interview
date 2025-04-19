from rest_framework.response import Response
from rest_framework.views import APIView

from .models import transaction_collection, transaction_summary_collection
from .queries import AggregateData, AggregateDataV2
from .serializers import AggregatedTransactionSerializer


class TransactionListAPIView(APIView):
    def get(self, request, *args, **kwargs):
        aggregator = AggregateData()
        merchant_id = request.GET.get('merchant_id')
        if merchant_id:
            aggregator.set_merchant_id(int(merchant_id))
        aggregator.set_mode(request.GET.get('mode'))
        aggregator.set_type(request.GET.get('type'))

        # Execute the aggregation
        results = transaction_collection.aggregate(aggregator.get_pipeline())
        serializer = AggregatedTransactionSerializer(results, many=True)
        return Response(serializer.data)


class TransactionListV2APIView(APIView):
    def get(self, request, *args, **kwargs):
        aggregator = AggregateDataV2()
        merchant_id = request.GET.get('merchant_id')
        if merchant_id:
            aggregator.set_merchant_id(int(merchant_id))
        aggregator.set_mode(request.GET.get('mode'))
        aggregator.set_type(request.GET.get('type'))
        aggregator.set_today_date('2024-12-10')
        results = aggregator.combine_documents(transaction_collection, transaction_summary_collection)
        serializer = AggregatedTransactionSerializer(results, many=True)
        return Response(serializer.data)
