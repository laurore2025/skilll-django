# Modèles de code (style maison)

Exemples tirés des projets existants, à adapter. Tous les noms métier sont en français.

## Application : `apps.py` et `urls.py`

```python
# apps/<app>/apps.py
from django.apps import AppConfig


class IntegrationsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.integrations"
    verbose_name = "Intégrations (csAdmin, DHIS2)"
```

```python
# apps/<app>/urls.py
from django.urls import path

from . import views

app_name = "core"

urlpatterns = [
    path("", views.home, name="home"),
    path("contact/", views.contact, name="contact"),
]
```

## Vue fonctionnelle avec amélioration progressive

Le formulaire fonctionne sans JavaScript (redirection) et avec `fetch` (réponse JSON).

```python
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views.decorators.http import require_POST

from .forms import ContactForm

CONTACT_MAX_PAR_HEURE = 5  # messages acceptés par adresse IP et par heure


def _ip(request):
    xff = request.META.get("HTTP_X_FORWARDED_FOR", "")   # ne s'y fier que derrière un proxy maîtrisé
    return (xff.split(",")[0].strip() if xff else request.META.get("REMOTE_ADDR")) or None


def _veut_json(request):
    return (request.headers.get("X-Requested-With") == "fetch"
            or "application/json" in request.headers.get("Accept", ""))


def _reponse(request, form, ok, code="", status=200):
    """JSON pour le formulaire envoyé par script, sinon page complète (sans JavaScript)."""
    if _veut_json(request):
        return JsonResponse({"ok": ok, "code": code, "erreurs": {} if ok else form.errors}, status=status)
    if ok:
        return redirect(reverse("core:home") + "?contact=ok#contact-form")
    return render(request, "core/home.html", {"contact_form": form, "contact_code": code}, status=status)


@require_POST
def contact(request):
    """Réception du formulaire de contact : contrôle anti-abus, enregistrement, envoi."""
    form = ContactForm(request.POST)
    cle = f"contact:{_ip(request)}"
    if cache.get(cle, 0) >= CONTACT_MAX_PAR_HEURE:
        return _reponse(request, form, False, "limite", 429)
    if not form.is_valid():
        return _reponse(request, form, False, "invalide", 400)
    form.save()
    cache.set(cle, cache.get(cle, 0) + 1, 3600)
    return _reponse(request, ContactForm(), True, "ok")
```

Côté JavaScript : `fetch(url, {method: "POST", body: new FormData(form), headers: {"X-Requested-With": "fetch"}})`.

## Formulaire public avec pot de miel

```python
from django import forms

from .models import MessageContact


class ContactForm(forms.ModelForm):
    """Formulaire de contact. Le champ « site » est un pot de miel : caché, rempli par les robots."""

    site = forms.CharField(required=False, widget=forms.HiddenInput)

    class Meta:
        model = MessageContact
        fields = ["nom", "email", "telephone", "sujet", "message"]

    def clean_site(self):
        if self.cleaned_data.get("site"):
            raise forms.ValidationError("Envoi refusé.")
        return ""

    def clean_message(self):
        message = (self.cleaned_data.get("message") or "").strip()
        if len(message) < 10:
            raise forms.ValidationError("Votre message est trop court (10 caractères minimum).")
        return message
```

## Configuration éditable dans l'admin (enregistrement unique)

```python
# models.py
class ConfigurationCourriel(models.Model):
    """Réglages d'envoi des courriels, modifiables dans l'admin (un seul enregistrement)."""

    actif = models.BooleanField("envoi par courriel activé", default=True)
    destinataires = models.CharField("destinataires", max_length=500, blank=True,
                                     help_text="Adresses séparées par des virgules.")
    modifie_le = models.DateTimeField("modifié le", auto_now=True)

    class Meta:
        verbose_name = "configuration du courriel"
        verbose_name_plural = "configuration du courriel"

    def __str__(self):
        return "Configuration du courriel"

    @classmethod
    def charger(cls):
        """L'enregistrement unique, créé à la première demande."""
        obj = cls.objects.first()
        return obj if obj is not None else cls.objects.create()
```

```python
# admin.py
@admin.register(ConfigurationCourriel)
class ConfigurationCourrielAdmin(admin.ModelAdmin):
    fieldsets = (("Réception des messages", {"fields": ("actif", "destinataires")}),)

    # un seul enregistrement : pas d'ajout ni de suppression, la liste renvoie au formulaire
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = ConfigurationCourriel.charger()
        return redirect(reverse("admin:core_configurationcourriel_change", args=[obj.pk]))
```

## Table héritée en lecture seule

```python
class Etablissement(models.Model):
    """Établissements de l'ancienne application (table historique, alimentée hors Django)."""

    sysid = models.AutoField(primary_key=True)
    nom = models.CharField(db_column="nameoffacility", max_length=255, blank=True, null=True)

    class Meta:
        managed = False            # Django lit la table, ne la crée ni ne la modifie
        db_table = "spa2017_new"
        verbose_name = "établissement"
```

```python
class ReadOnlyAdmin(admin.ModelAdmin):
    """Consultation seule des tables historiques."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
```

## Table PostGIS créée par migration SQL (sans GeoDjango)

```python
"""Table des contours administratifs (PostGIS). Créée en SQL : la colonne geom n'est pas
déclarée dans le modèle (managed = False). Les données sont importées par import_boundaries."""
from django.db import migrations

CREATE = """
CREATE EXTENSION IF NOT EXISTS postgis;   -- à créer au préalable par un superutilisateur
CREATE TABLE IF NOT EXISTS geography_boundary (
    id          bigserial PRIMARY KEY,
    level       varchar(20)  NOT NULL,
    name        varchar(150) NOT NULL,
    imported_at timestamptz  NOT NULL DEFAULT now(),
    geom        geometry(MultiPolygon, 4326)
);
CREATE INDEX IF NOT EXISTS geography_boundary_geom_idx ON geography_boundary USING GIST (geom);
"""
DROP = "DROP TABLE IF EXISTS geography_boundary;"


class Migration(migrations.Migration):
    dependencies = [("geography", "0001_initial")]
    operations = [migrations.RunSQL(CREATE, DROP)]
```

Requête spatiale paramétrée :

```python
from django.db import connection


def etablissements_proches(lat, lng, rayon_km):
    """Établissements à moins de rayon_km du point, du plus proche au plus éloigné."""
    sql = (
        "SELECT facility_id, nameoffacility, "
        "ST_Distance(geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography) / 1000.0 AS dist "
        "FROM facilities_facilitygeometry "
        "WHERE ST_DWithin(geom::geography, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, %s) "
        "ORDER BY dist"
    )
    with connection.cursor() as cur:
        cur.execute(sql, [lng, lat, lng, lat, rayon_km * 1000])
        return cur.fetchall()
```

Colonne choisie par l'utilisateur : la valider contre une **liste blanche** avant de l'insérer
dans le SQL, jamais par concaténation directe.

## Intégration externe : client, copie locale, état

```python
# models.py
class SourceItem(models.Model):
    """Copie locale d'un élément de la source externe (l'affichage ne lit que cette copie)."""

    ressource = models.CharField("ressource", max_length=50)
    id_source = models.CharField("identifiant dans la source", max_length=100)
    contenu = models.JSONField("contenu")
    synchronise_le = models.DateTimeField("synchronisé le", auto_now=True)

    class Meta:
        unique_together = [("ressource", "id_source")]


class SourceSync(models.Model):
    """État de synchronisation d'une ressource."""

    ressource = models.CharField("ressource", max_length=50, unique=True)
    nombre = models.PositiveIntegerField("nombre d'éléments", default=0)
    derniere_tentative = models.DateTimeField("dernière tentative", null=True, blank=True)
    derniere_reussite = models.DateTimeField("dernière réussite", null=True, blank=True)
    derniere_erreur = models.TextField("dernière erreur", blank=True)
```

```python
# sync.py
import json
import logging
import urllib.request

from django.conf import settings
from django.db import transaction
from django.utils import timezone

from .models import SourceItem, SourceSync

log = logging.getLogger(__name__)


def _lire(url):
    req = urllib.request.Request(url, headers={"Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=30) as resp:     # délai toujours explicite
        return json.loads(resp.read().decode("utf-8"))


def synchroniser(ressource):
    """Recopie une ressource. Renvoie (nombre d'éléments, erreur ou ''). Un échec garde la copie."""
    etat, _ = SourceSync.objects.get_or_create(ressource=ressource)
    etat.derniere_tentative = timezone.now()
    try:
        donnees = _lire(f"{settings.SOURCE_URL}/{ressource}/")
    except Exception as exc:  # noqa: BLE001 - l'erreur est journalisée et conservée
        etat.derniere_erreur = str(exc)[:1000]
        etat.save()
        log.warning("synchronisation %s : %s", ressource, exc)
        return etat.nombre, etat.derniere_erreur
    with transaction.atomic():
        vus = []
        for element in donnees:
            SourceItem.objects.update_or_create(
                ressource=ressource, id_source=str(element["id"]), defaults={"contenu": element})
            vus.append(str(element["id"]))
        SourceItem.objects.filter(ressource=ressource).exclude(id_source__in=vus).delete()
        etat.nombre, etat.derniere_reussite, etat.derniere_erreur = len(vus), timezone.now(), ""
        etat.save()
    return len(vus), ""
```

## Commande de gestion avec boucle

```python
"""
Commande : python manage.py sync_source [--loop] [--interval 300]

Synchronise la source externe dans la base locale. En production, lancée en boucle par un
service Docker (ou par cron sans --loop).
"""
import time

from django.core.management.base import BaseCommand, CommandError

from apps.integrations import sync

RESSOURCES = ("communes", "etablissements")


class Command(BaseCommand):
    help = "Synchronise la source externe dans la base locale."

    def add_arguments(self, parser):
        parser.add_argument("--loop", action="store_true", help="répéter indéfiniment")
        parser.add_argument("--interval", type=int, default=300, help="secondes entre deux passages")

    def handle(self, *args, **options):
        while True:
            erreurs = []
            for ressource in RESSOURCES:
                nombre, erreur = sync.synchroniser(ressource)
                if erreur:
                    erreurs.append(ressource)
                    self.stderr.write(f"{ressource} : ERREUR {erreur} ({nombre} élément(s) conservés)")
                else:
                    self.stdout.write(f"{ressource} : {nombre} élément(s)")
            if not options["loop"]:
                if erreurs:
                    raise CommandError("échec pour : " + ", ".join(erreurs))
                return
            time.sleep(options["interval"])
```

## Requêtes REST Client (`http/NN_sujet.http`)

```http
@host = http://localhost:8000

### Accueil
# Attendu : 200, page HTML avec le formulaire de contact
GET {{host}}/

### Formulaire de contact sans jeton CSRF
# Attendu : 403 (protection CSRF)
POST {{host}}/contact/
Content-Type: application/x-www-form-urlencoded

nom=Test&email=test@example.org&sujet=Essai&message=Message de test assez long

### API : départements
# Attendu : 200, GeoJSON avec 10 entités
GET {{host}}/cartographie/api/departements.geojson
```

## Traduction côté client (créole)

```html
<h2 data-i18n="contact.titre">Nous contacter</h2>
<script src="{% static 'js/traductions/accueil.ht.js' %}"></script>
```

```javascript
// static/js/traductions/accueil.ht.js — textes en créole haïtien, clés = attributs data-i18n
window.TRADUCTIONS_HT = Object.assign(window.TRADUCTIONS_HT || {}, {
  "contact.titre": "Kontakte nou",
});
```
