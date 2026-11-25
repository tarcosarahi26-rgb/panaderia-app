from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import Group
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from panaderia.forms import RegistroForm
from panaderia.utils.grupos import GRUPO_CONSULTOR


def registro_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Todo usuario nuevo entra al grupo con menos privilegios.
            grupo, _ = Group.objects.get_or_create(name=GRUPO_CONSULTOR)
            user.groups.add(grupo)
            login(request, user)
            messages.success(request, f"¡Bienvenido, {user.username}! Tu cuenta fue creada.")
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = RegistroForm()
    return render(request, "panaderia/auth/registro.html", {"form": form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect(settings.LOGIN_REDIRECT_URL)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            messages.success(request, "Has iniciado sesión correctamente.")
            siguiente = request.POST.get("next", "")
            if siguiente and url_has_allowed_host_and_scheme(
                siguiente, allowed_hosts={request.get_host()}
            ):
                return redirect(siguiente)
            return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        form = AuthenticationForm(request)
    return render(
        request,
        "panaderia/auth/login.html",
        {"form": form, "next": request.GET.get("next", "")},
    )


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Sesión cerrada.")
    return redirect(settings.LOGOUT_REDIRECT_URL)
