def profile_photo_advisor(request):
    data=request.FILES.get('file')

    advisor = request.user.advisor_user
    if advisor.profile_photo_advisor:
        advpath = advisor.profile_photo_advisor.url.split(settings.MEDIA_URL)
        os.remove(os.path.join(settings.MEDIA_ROOT,advpath[1]))
    #data.name = str(request.user.id) + "_apfp"
    advisor.profile_photo_advisor=data
    advisor.save()

    data = {
        'ok' : 'ok',
    }
    return JsonResponse(data)