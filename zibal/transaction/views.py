from rest_framework.response import Response
from rest_framework.views import APIView

from .models import transaction_collection
from .queries import AggregateData
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
