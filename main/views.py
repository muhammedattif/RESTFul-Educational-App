from django.shortcuts import render, HttpResponse
from admin_analytics.models import AggregateCard

def test(request):
    cards = AggregateCard.objects.all()
    print(cards[0])
    print(cards[0].execute())
    print(cards[1])
    print(cards[1].execute())
    print(cards[2])
    print(cards[2].execute())
