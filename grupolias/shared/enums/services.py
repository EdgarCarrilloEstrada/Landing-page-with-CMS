from django.db import models

class Services(models.TextChoices):
    PLUMBING = "plomeria", "Plomería"
    ELECTRICITY = "electricidad", "Electricidad"
    GLASS_AND_ALUMINUM = "vidrio y aluminio", "Vidrio y aluminio"
    BLACKSMITHING = "herreria", "Herrería"
    INFORMATION_GATHERING = "levantamiento de informacion", "Levantamiento de información"
    CARPENTRY = "carpinteria", "Carpintería"
    WATERPROOFING = "impermeabilizacion", "Impermeabilización"
    PAINTING = "pintura", "Pintura"
    REMODELING = "remodelacion", "Remodelación"
    EXPANSION = "ampliacion", "Ampliación"
    AIR_CONDITIONING = "aire acondicionado", "Aire acondicionado"
    LOCKSMITHING = "cerrajería", "Cerrajería"
    DESIGN = "diseño", "Diseño"
    PROJECT = "proyecto", "Proyecto"