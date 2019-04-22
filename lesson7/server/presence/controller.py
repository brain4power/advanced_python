from protocol import make_response, make_400


def get_presence(request):
    user = request.get('user')
    if user:
        account_name = user.get('account_name')
        status = user.get('status')
        if account_name and status:
            return make_response(
                request, 200
            )

    return make_400(request)
