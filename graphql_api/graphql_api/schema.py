import graphene
from graphene_django import DjangoObjectType
from graphene_django.debug import DjangoDebug
from graphql_api.transaction.schema import TransactionQueries

from monit.models import Transaction

from datetime import datetime, timedelta


class TransactionType(DjangoObjectType):
    class Meta:
        model = Transaction
        fields = ("category", "amount")


class Query(TransactionQueries):

    transactions = graphene.List(TransactionType, presetRange=graphene.String())
    debug = graphene.Field(DjangoDebug, name="_debug")

    def resolve_transactions(root, info, presetRange=None):

        if presetRange == "LAST_7_DAYS":
            return Transaction.objects.filter(
                created_at__gte=datetime.now() - timedelta(days=7)
            )
        elif presetRange == "LAST_7_WEEKS":
            return Transaction.objects.filter(
                created_at__gte=datetime.now() - timedelta(weeks=7)
            )
        elif presetRange == "LAST_7_MONTHS":
            return Transaction.objects.filter(
                created_at__gte=datetime.now() - timedelta(weeks=30)
            )
        else:
            return None


schema = graphene.Schema(query=Query)
