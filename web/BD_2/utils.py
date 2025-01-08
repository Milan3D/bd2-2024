class LocalStorage:
    @staticmethod
    def set_id_nivel(request, id_nivel):
        request.session['id_nivel'] = id_nivel

    @staticmethod
    def get_id_nivel(request):
        return request.session.get('id_nivel', None)