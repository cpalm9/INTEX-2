def LastFiveMiddleware(get_response):
    # One-time configuration and initialization.

    firstTime = {'value': True}

    def middleware(request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        #pull last five list out of session
        last5_list = request.session.get('last5')
        if last5_list is None or firstTime['value']:
            last5_list = []
        firstTime['value'] = False

         #let django continue
        request.last5 = last5_list

        response = get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        #
        # request.session['last5'] = request.last5[:5]

        return response

    return middleware