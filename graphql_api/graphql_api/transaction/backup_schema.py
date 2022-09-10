import graphene
from graphql_api.transaction.models import Transaction
from graphene import Node
from graphene_django.types import DjangoObjectType, ObjectType
from datetime import datetime, timedelta
from django.db.models import Sum

class TransactionNode(DjangoObjectType):
    class Meta:
        model = Transaction
        interfaces = (Node,)
        fields = "__all__"
        filter_fields = []

    pk = graphene.String()


# class PresetRangeType(DjangoObjectType):
#     class Meta:
#         model = Transaction
#         fields = ('category', 'amount')

#     category = graphene.String()
#     amount = graphene.Float()

#     extra_field = graphene.String()

#     def resolve_category(self, info):
#         return "hello!"


class PresetRangeType(graphene.ObjectType):
    category = graphene.String()
    amount = graphene.Float()


class TransactionQueries(graphene.ObjectType):
    transactions = graphene.List(TransactionNode)

    def resolve_transactions(self, info):
        return Transaction.objects.all().order_by("-created_at")


class GetTransactionStatsQueries(graphene.ObjectType):
    transactions_stats = graphene.List(PresetRangeType, presetRange=graphene.String())
    # transactions_stats = graphene.List(PresetRangeType)

    def resolve_transactions_stats(self, info, presetRange):

        if presetRange == "LAST_7_DAYS":
            today = datetime.now()
            seven_day_before = str(today - timedelta(days=7))
            # print(seven_day_before, "---", flush=True)
            # result = Transaction.objects.all().order_by("-created_at")
            # result = Transaction.objects.filter(created_at__gte=seven_day_before).aggregate(Sum('amount'))
            result = Transaction.objects.filter(created_at__gte=seven_day_before).values('category').order_by('category').annotate(amount=Sum('amount'))
            # result = Transaction.objects.filter(created_at__gte=seven_day_before).order_by('category').aggregate(Sum('amount'))
            print(result, "-----")
            # PresetRangeType.category = result["category"]
            # PresetRangeType.amount = result["amount"]
            #     filter(created_at__gte=seven_day_before).aggregate(Sum('amount'))
            # print(result, flush=True)
            resp = []
            for res in result:
                resp.append(res)
            return list(result)


class GetTransactionSeriesQueries(graphene.ObjectType):
    transactions_series = graphene.List(PresetRangeType, presetRange=graphene.String())
    # transactions_stats = graphene.List(PresetRangeType)

    def resolve_transactions_series(self, info, presetRange):

        # if presetRange == "LAST_7_DAYS":
        today = datetime.now()
        seven_day_before = str(today - timedelta(days=7))
        # print(seven_day_before, "---", flush=True)
        # result = Transaction.objects.all().order_by("-created_at")
        # result = Transaction.objects.filter(created_at__gte=seven_day_before).aggregate(Sum('amount'))
        result = Transaction.objects.values('amount').order(created_at__gte=seven_day_before).aggregate(Sum('amount'))
        print(result, flush=True)
        return result





    # EXTEND THIS CODE