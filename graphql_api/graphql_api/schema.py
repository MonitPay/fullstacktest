import graphene
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphql_api.transaction.schema import TransactionQueries

from monit.models import Transaction

from datetime import datetime, timedelta
from django.db.models import Sum


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ("category", "amount")

    sum = graphene.Int()


class Query(TransactionQueries):

    transactions = graphene.List(TransactionType, presetRange=graphene.String())
    # transactions = graphene.String(presetRange=graphene.String())

    debug = graphene.Field(DjangoDebug, name="_debug")

    def resolve_transactions(root, info, presetRange=None):

        if presetRange == "LAST_7_DAYS":
            query = (
                Transaction.objects.filter(
                    created_at__gte=datetime.now() - timedelta(days=7)
                )
                .values("category")
                .order_by("category")
                .annotate(amount=Sum("amount"))
            )
            print(query)
            return None
        elif presetRange == "LAST_7_WEEKS":
            query = (
                Transaction.objects.filter(
                    created_at__gte=datetime.now() - timedelta(weeks=7)
                )
                .values("category")
                .order_by("category")
                .annotate(amount=Sum("amount"))
            )
            print(query)
            return None
        elif presetRange == "LAST_7_MONTHS":
            query = (
                Transaction.objects.filter(
                    created_at__gte=datetime.now() - timedelta(weeks=30)
                )
                .values("category")
                .order_by("category")
                .annotate(amount=Sum("amount"))
            )
            print(query)
            return None
        else:
            return None

    def resolve_hello(root, info, name):
        return f"Hello {name}!"


schema = graphene.Schema(query=Query)
