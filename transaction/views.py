from django.shortcuts import render


# Create your views here.

def sale(request):
    # projects = Project.objects.order_by('-date')
    # categories = Project.objects.values_list('type').distinct().order_by('-date')
    # catg = set()
    # for category in categories:
    #
    #     cat = ' '.join(category)
    #     c = cat.split()
    #     for a in c:
    #         catg.add(a)
    # data = {
    #     'projects': projects,
    #     'categories': catg
    # }
    return render(request, "transaction/index.html")
