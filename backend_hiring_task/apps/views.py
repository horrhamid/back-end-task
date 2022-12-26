from .serializers import AppsSerializer, DictySerializer
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.views import APIView
import os
from .models import Apps, Dicty


class AppsView(APIView):

    def post(self, request):
        data = request.data
        print(data)
        apps_ser = AppsSerializer(data={"name": data["name"], "image": data["image"], "command": data["command"]})
        if apps_ser.is_valid():
            app_name = apps_ser.save()
        else:
            return Response(apps_ser.errors, 400)

        app = Apps.objects.filter(name=app_name)[0]

        if "envs" in data:
            for key in data["envs"]:
                dict_ser = DictySerializer(data={"key": key, "value": data["envs"][key], "app": app.pk})
                if dict_ser.is_valid():
                    dict_ser.save()
                else:
                    return Response(dict_ser.errors, 400)

        return Response(data={"status": "done"})

    def get(self, request):
        app = Apps.objects.all()
        data = [a.name for a in app]
        ser = AppsSerializer(app, many=True)
        return Response(ser.data)


class AppView(APIView):

    def get(self, request, app_id, **kwargs):
        app = Apps.objects.filter(id=app_id)
        data = [a.name for a in app]
        ser = AppsSerializer(app, many=True)
        return Response(ser.data)


class AppRunView(APIView):
    def post(self, request, app_id, **kwargs):
        app = Apps.objects.filter(id=app_id)[0]
        envs = Dicty.objects.filter(app_id=app.pk)
        command = "docker  run -d"
        for env in envs:
            command += " -e " + env.key + "=" + env.value

        command += " --name " + app.name + "_v" + str(app.version) + " " + app.image + " " + app.command
        app.version = app.version + 1
        app.save()
        return_value = os.system(command)
        return Response(str(return_value) + " " + command)

