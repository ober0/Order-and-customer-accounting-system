from django.http import JsonResponse
from django.shortcuts import render, redirect


def main(request):
    return redirect('/orders/')