from .serializers import AppsSerializer, DictySerializer
from rest_framework.response import Response
from rest_framework.views import APIView
import docker
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

        return Response({"Status": "done", "ID": str(app.pk)})

    def get(self, request, **kwargs):
        app = Apps.objects.all()
        ser = AppsSerializer(app, many=True)

        return Response(ser.data)


class AppView(APIView):

    def get(self, request, app_id, **kwargs):
        app = Apps.objects.filter(id=app_id)
        ser = AppsSerializer(app, many=True)

        return Response(ser.data)

    def delete(self, request, app_id, **kwargs):
        app = Apps.objects.filter(id=app_id)
        app.delete()

        return Response("App deleted!")

    def put(self, request, app_id, **kwargs):
        app = Apps.objects.get(pk=app_id)
        data = request.data
        apps_ser = AppsSerializer(app, data={"name": data["name"], "image": data["image"], "command": data["command"]})
        if apps_ser.is_valid():
            apps_ser.save()
        else:
            return Response(apps_ser.errors, 400)

        dicts = Dicty.objects.filter(app_id=app.pk)
        for dic in dicts:
            dic.delete()
        
        if "envs" in data:
            for key in data["envs"]:
                dict_ser = DictySerializer(data={"key": key, "value": data["envs"][key], "app": app.pk})
                if dict_ser.is_valid():
                    dict_ser.save()
                else:
                    return Response(dict_ser.errors, 400)
        return Response(apps_ser.data)


class AppRunView(APIView):

    def post(request, app_id, **kwargs):
        app = Apps.objects.filter(id=app_id)[0]
        envs = Dicty.objects.filter(app_id=app.pk)
        client = docker.from_env()
        environments = {}

        for env in envs:
            environments[env.key] = env.value

        container = client.containers.run(app.image, app.command, name=(app.name + "__v" + str(app.version)),
                                          labels=environments, environment=environments, detach=True)
        app.version = app.version + 1
        app.save()
        return Response("Done!")


class AppHistoryView(APIView):

    def post(request, app_id, **kwargs):
        app = Apps.objects.filter(id=app_id)[0]
        app_name = app.name
        client = docker.from_env()
        containers_list = client.containers.list(all=True)

        context = {}

        for container in containers_list:
            temp = {}
            if container.attrs["Name"].split("__v")[0][1:] == app_name:
                temp["Name"] = container.attrs["Name"][1:]
                temp["Status"] = container.attrs["State"]["Status"]
                temp["Started"] = container.attrs["State"]["StartedAt"]
                if temp["Status"] == "running":
                    temp["Finished"] = "-1"
                else:
                    temp["Finished"] = container.attrs["State"]["FinishedAt"]
                temp["Image"] = container.attrs["Config"]["Image"]
                temp["Envs"] = container.attrs["Config"]["Env"]
                temp["Args"] = container.attrs["Args"]

                context[container.id] = temp

        return Response(context)
