from dataclasses import Field
from email.policy import default
from django import forms
from django.db import models
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from wagtail.core.models import Page, Orderable
from wagtail.search import index
from django.core.validators import MaxLengthValidator
from django.core import validators
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.snippets.models import register_snippet
from wagtail.contrib.settings.models import BaseSetting, register_setting


@register_setting
class header(BaseSetting):
    id = models.AutoField(primary_key=True)
    Logo_barra_de_navegación = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Navegación_1 = models.CharField(max_length=8, blank=False, null=False, default="Inicio")
    Navegación_2 = models.CharField(max_length=11, blank=False, null=False, default="Servicios")
    Navegación_3 = models.CharField(max_length=11, blank=False, null=False, default="Conócenos")
    Navegación_4 = models.CharField(max_length=11, blank=False, null=False, default="Contáctanos")

    panels = [
        ImageChooserPanel("Logo_barra_de_navegación"),
        FieldPanel("Navegación_1"),
        FieldPanel("Navegación_2"),
        FieldPanel("Navegación_3"),
        FieldPanel("Navegación_4"),
    ]

@register_setting
class footer(BaseSetting):
    id = models.AutoField(primary_key=True)
    Nombre_de_la_empresa = models.CharField(max_length=15, blank=False, null=False, default="Grupo LIAS")
    Dirección_de_la_empresa = models.CharField(max_length=100, blank=False, null=False, default="C. Pisperama 180-interior. 6, Vista Bella, 58090 Morelia, Mich.")
    Título_sección_izquierda = models.CharField(max_length=20, blank=False, null=False, default="OTROS ENLACES")
    Enlace_1 = models.CharField(max_length=20, blank=False, null=False, default="Conócenos")
    Enlace_2 = models.CharField(max_length=20, blank=False, null=False, default="Preguntas frecuentes")
    Enlace_3 = models.CharField(max_length=20, blank=False, null=False, default="Comentarios")
    Título_sección_derecha = models.CharField(max_length=20, blank=False, null=False, default="CONTACTO")
    Enlace_4 = models.CharField(max_length=20, blank=False, null=False, default="Contáctanos")
    Celular = models.CharField(max_length=16, blank=False, null=False, default="443-471-4356")
    Link_a_celular = models.CharField(max_length=13, blank=False, null=False, default="4434714356")
    Teléfono = models.CharField(max_length=16, blank=False, null=False, default="554-833-5729")
    Link_a_teléfono = models.CharField(max_length=13, blank=False, null=False, default="+525548335729")
    Enlace_5 = models.CharField(max_length=40, blank=False, null=False, default="grupolias@hotmail.com")
    Título_sección_de_redes = models.CharField(max_length=40, blank=False, null=False, default="SIGUENOS EN NUESTRAS REDES")
    Logo_red_social1 = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = "+"
    )
    Link_a_red_social1 = models.CharField(max_length=200, blank=False, null=False, default="https://www.facebook.com/GRUPOLIAS")
    Logo_red_social2 = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = "+"
    )
    Link_a_red_social2 = models.CharField(max_length=200, blank=False, null=False, default="https://www.instagram.com/gpolias2000/?hl=es")

    panels = [
        FieldPanel("Nombre_de_la_empresa"),
        FieldPanel("Dirección_de_la_empresa"),
        FieldPanel("Título_sección_izquierda"),
        FieldPanel("Enlace_1"),
        FieldPanel("Enlace_2"),
        FieldPanel("Enlace_3"),
        FieldPanel("Título_sección_derecha"),
        FieldPanel("Enlace_4"),
        MultiFieldPanel([
            FieldPanel("Celular"),
            FieldPanel("Link_a_celular")
            ], heading="Medio por celular"
        ),
        MultiFieldPanel([
            FieldPanel("Teléfono"),
            FieldPanel("Link_a_teléfono")
            ], heading="Medio por teléfono"
        ),
        FieldPanel("Enlace_5"),
        FieldPanel("Título_sección_de_redes"),
        MultiFieldPanel([
            ImageChooserPanel("Logo_red_social1"),
            FieldPanel("Link_a_red_social1")
            ], heading="Red social 1"
        ),
        MultiFieldPanel([
            ImageChooserPanel("Logo_red_social2"),
            FieldPanel("Link_a_red_social2")
            ], heading="Red social 2"
        ),
    ]

@register_setting
class Plantilla_servicios(BaseSetting):
    id = models.AutoField(primary_key=True)
    Título_trabajos_hechos = models.CharField(max_length=40, blank=False, null=False, default="")

    Título_sección_cotizar = models.CharField(max_length=40, blank= False, null=False, default="")

    Título_cuadro_1 = models.CharField(max_length=24, blank=False, null=False, default="")
    Icono_cuadro_1 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    Descripción_cuadro_1 = RichTextField(blank=False, validators=[MaxLengthValidator(280)] ,features=['bold' ,'italic', 'ol', 'ul', 'hr'])

    Título_cuadro_2 = models.CharField(max_length=24, blank=False, null=False, default="")
    Icono_cuadro_2 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    Descripción_cuadro_2 = RichTextField(blank=False, validators=[MaxLengthValidator(130)], features=['bold' ,'italic', 'ol', 'ul', 'hr'])
    Boton_cuadro_2 = models.CharField(max_length=15, blank=False, null=False, default="")

    Título_cuadro_3 = models.CharField(max_length=24, blank=False, null=False, default="")
    Icono_cuadro_3 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    Descripción_cuadro_3 = RichTextField(blank=False, validators=[MaxLengthValidator(130)], features=['bold' ,'italic', 'ol', 'ul', 'hr'])
    Boton_cuadro_3 = models.CharField(max_length=15, blank=False, null=False, default="")

    panels = [
        FieldPanel("Título_trabajos_hechos"),
        MultiFieldPanel([
            FieldPanel("Título_sección_cotizar"),
            MultiFieldPanel([
                FieldPanel("Título_cuadro_1"),
                ImageChooserPanel("Icono_cuadro_1"),
                FieldPanel("Descripción_cuadro_1", classname="full"),
                ],
                heading= "Cuadro 1",
            ),
            MultiFieldPanel([
                FieldPanel("Título_cuadro_2"),
                ImageChooserPanel("Icono_cuadro_2"),
                FieldPanel("Descripción_cuadro_2", classname="full"),
                FieldPanel("Boton_cuadro_2"),
                ],
                heading= "Cuadro 2",
            ),
            MultiFieldPanel([
                FieldPanel("Título_cuadro_3"),
                ImageChooserPanel("Icono_cuadro_3"),
                FieldPanel("Descripción_cuadro_3", classname="full"),
                FieldPanel("Boton_cuadro_3"),
                ],
                heading= "Cuadro 3",
            ),
            ],
            heading="Sección de cotización",
        ),
    ]

# class PreguntasCategory(models.Model):

#     id = models.AutoField(primary_key=True)
#     nombre= models.CharField(max_length=50)
#     Identificador= models.SlugField(verbose_name="Identificador", allow_unicode=True, max_length=50, help_text="Nombre para identificar a esta categoria", null= True)
    
#     panels = [
#         FieldPanel("nombre"),
#         FieldPanel("Identificador")
#     ]

#     class Meta:
#         verbose_name="Categoria pregunta"
#         verbose_name_plural="Categoria preguntas"
#         ordering = ["nombre"]

#     def __str__(self):
#         return self.nombre

# register_snippet(PreguntasCategory)

class HomePage(Page):
    max_count=1

    Texto_de_bienvenida = models.CharField(max_length=200, blank=False, null=False, default="")
    Imagen_de_bienvenida = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    Imagen_categoría_1 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    Imagen_categoría_2 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    Imagen_categoría_3 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    Imagen_categoría_4 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Separador_servicios = models.CharField (max_length=50, blank=False, null=False, default="")
    Separador_anuncios = models.CharField (max_length=50, blank=False, null=False, default="")

    Imagen_izq = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Titulo_izq = models.CharField (max_length=40, blank=False, null=False, default="")
    Texto_izq = models.CharField (max_length=120, blank=False, null=False, default="")

    Imagen_der = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Titulo_der = models.CharField (max_length=40, blank=False, null=False, default="")
    Texto_der = models.CharField (max_length=120, blank=False, null=False, default="")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [InlinePanel("carousel_images", max_num=5, min_num=1, label="Image")],
            heading="Carousel Images",
        ),
        MultiFieldPanel([
            ImageChooserPanel("Imagen_de_bienvenida"),
            FieldPanel("Texto_de_bienvenida"),],
            heading="Descripcion del cuadro de bienvenida",
        ),
        MultiFieldPanel([
            ImageChooserPanel("Imagen_categoría_1"),
            ImageChooserPanel("Imagen_categoría_2"),
            ImageChooserPanel("Imagen_categoría_3"),
            ImageChooserPanel("Imagen_categoría_4"),],
            heading = "Imágenes de los cuadros de categorías"
        ),
        MultiFieldPanel([
            FieldPanel("Separador_servicios"),],
            heading="Sección de servicios",
        ),
        MultiFieldPanel([
            FieldPanel("Separador_anuncios"),
            MultiFieldPanel([
                ImageChooserPanel("Imagen_izq"),
                FieldPanel("Titulo_izq"),
                FieldPanel("Texto_izq"),
                ],
                heading= "Imagen Izquierda",
            ),
            MultiFieldPanel([
                ImageChooserPanel("Imagen_der"),
                FieldPanel("Titulo_der"),
                FieldPanel("Texto_der"),
                ],
                heading= "Imagen Derecha",
            ),
            ],
            heading="Sección de anuncios",
        ),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        servicios = self.get_children().exact_type(ServiciosPage).live()
        context['servicios'] = servicios
        first_element = context['servicios'].first()
        context['categorias'] = first_element.specific.ServicioCategory.labels
        return context

class HomePageCarouselImages(Orderable):
    id = models.AutoField(primary_key=True)
    page = ParentalKey(HomePage, on_delete=models.CASCADE, related_name='carousel_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )
    Titulo_slide = models.CharField (max_length=50, blank = False, null = False)
    Texto_slide = models.CharField (max_length=150, blank = False, null = False)

    panels = [
        ImageChooserPanel('image'),
        FieldPanel('Titulo_slide'),
        FieldPanel('Texto_slide'),
    ]

class ServiciosPage(Page):
    subpage_types = []

    Imagen_principal_del_servicio = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    Descripción_servicio = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'], default="")

    class ServicioCategory(models.TextChoices):
        HOGAR = "HOGAR", "HOGAR"
        ELECTRICIDAD = "ELECTRICIDAD", "ELECTRICIDAD"
        PINTURA = "PINTURA", "PINTURA"
        CONSTRUCCION = "CONSTRUCCIÓN", "CONSTRUCCIÓN"
        

    category = models.TextField(
        max_length=12,
        choices=ServicioCategory.choices,
        default=ServicioCategory.HOGAR
    )

    search_fields = Page.search_fields + [
        index.SearchField('Descripción_servicio'),
    ]

    Título_de_ventana = models.CharField(max_length=25, blank=False, null=False, default="COTIZACIONES")
    
    Descripción_1 = RichTextField(blank=False, features=['bold' ,'italic'], default="Es posible que el precio cambie dependiendo del tipo de trabajo que se requiera, estos son solo precios de referencia")
    
    Título_columna_1 = models.CharField(max_length=15, blank=False, null=False, default="Actividad")
    Texto_1_columna_1 = models.CharField(max_length=35, blank=False, null=False, default="Visita")
    Texto_2_columna_1 = models.CharField(max_length=35, blank=False, null=False, default="Servicios de mano de obra")
    
    Título_columna_2 = models.CharField(max_length=15, blank=False, null=False, default="Precio")
    Texto_1_columna_2 = models.CharField(max_length=35, blank=False, null=False, default="$200")
    Texto_2_columna_2 = models.CharField(max_length=12, blank=False, null=False, default="$400")
    
    Descripción_2 = RichTextField(blank=False, features=['bold' ,'italic'], default="*Si aceptan la cotización/el servicio, se descuenta el precio de visita")    

    content_panels = Page.content_panels + [
        ImageChooserPanel("Imagen_principal_del_servicio"),
        FieldPanel('Descripción_servicio', classname="full"),
        FieldPanel("category", widget=forms.Select),
        MultiFieldPanel(
            [InlinePanel("servicios_images", max_num=6, min_num=1, label="Imagen")],
            heading="Imágenes de servicios realizados",
        ),
        MultiFieldPanel(
            [
                FieldPanel("Título_de_ventana"),
                FieldPanel('Descripción_1', classname="full"),
                FieldPanel("Título_columna_1"),
                FieldPanel("Texto_1_columna_1"),
                FieldPanel("Texto_2_columna_1"),
                FieldPanel("Título_columna_2"),
                FieldPanel("Texto_1_columna_2"),
                FieldPanel("Texto_2_columna_2"),
                FieldPanel('Descripción_2', classname="full"),
            ],
            heading = "Ventana de cotizar"
        )
    ]

class ServiciosImages(Orderable):
    id = models.AutoField(primary_key=True)
    page = ParentalKey(ServiciosPage, on_delete=models.CASCADE, related_name='servicios_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]

class ConocenosPage(Page):
    max_count=1

    subpage_types = []

    Logo_en_el_cuadro = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Texto_del_cuadro = models.CharField(max_length=150, blank=False, null=False, default="")
    
    Título_del_mapa = models.CharField(max_length=60, blank=False, null=False, default="")
    
    Título_principal = models.CharField(max_length=40, blank=False, null=False, default="")
    Texto_principal = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'])

    Primer_título = models.CharField(max_length=40 , blank=False, null=False, default="")
    Texto_1er_título = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'])
    Imagen_1er_título = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    Segundo_título = models.CharField(max_length=40, blank=False, null=False, default="")
    Texto_2ndo_título = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'])
    Imagen_2ndo_título = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )

    Tercer_título = models.CharField(max_length=40, blank=False, null=False, default="")
    Texto_3er_título = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'])
    Imagen_3er_título = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    
    Separador_colab = models.CharField (max_length=50, blank=False, null=False, default="")
    Texto1 = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'])
    Texto2 = RichTextField(blank=False, features=['bold' ,'italic', 'ol', 'ul', 'hr'], null= False, default="")

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            ImageChooserPanel("Logo_en_el_cuadro"),
            FieldPanel("Texto_del_cuadro"),],
            heading="Cuadro de conocenos",
        ),
        MultiFieldPanel([
            FieldPanel("Título_del_mapa"),],
            heading="Sección de del mapa",
        ),
        MultiFieldPanel([
            FieldPanel("Título_principal"),
            FieldPanel("Texto_principal", classname="full"),],
            heading="Descripción principal",
        ),
        MultiFieldPanel([
            FieldPanel("Primer_título"),
            FieldPanel("Texto_1er_título", classname="full"),
            ImageChooserPanel("Imagen_1er_título"),
            ],
            heading="Primer apartado",
        ),
        MultiFieldPanel([
            FieldPanel("Segundo_título"),
            FieldPanel("Texto_2ndo_título", classname="full"),
            ImageChooserPanel("Imagen_2ndo_título"),
            ],
            heading="Segundo apartado",
        ),
        MultiFieldPanel([
            FieldPanel("Tercer_título"),
            FieldPanel("Texto_3er_título", classname="full"),
            ImageChooserPanel("Imagen_3er_título"),
            ],
            heading="Tercer apartado",
        ),
        MultiFieldPanel([
            FieldPanel("Separador_colab"),
            FieldPanel("Texto1", classname="full"),
            FieldPanel("Texto2", classname="full"),
            ],
            heading="Ultima sección"
        ),
        MultiFieldPanel(
            [InlinePanel("slider_images", max_num=7, min_num=3, label="Image")],
            heading="Imagenes del slider",
        ),
    ]


class ConocenosPageSlider(Orderable):
    id = models.AutoField(primary_key=True)
    page = ParentalKey(ConocenosPage, on_delete=models.CASCADE, related_name='slider_images')
    image = models.ForeignKey(
        'wagtailimages.Image', on_delete=models.CASCADE, related_name='+'
    )

    panels = [
        ImageChooserPanel('image'),
    ]
    
class ContactPage(Page):
    max_count=1

    subpage_types = []
    
    Imagen_Red_Social_1 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Usuario_Red_Social_1 = models.CharField(max_length=20, blank=False, null=False, default="")
    Link_a_Red_Social_1 = models.CharField(max_length=200, blank=False, null=False, default="https://www.instagram.com/gpolias2000/?hl=es")
    Imagen_Red_Social_2 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Usuario_Red_Social_2 = models.CharField(max_length=20, blank=False, null=False, default="")
    Link_a_Red_Social_2 = models.CharField(max_length=200, blank=False, null=False, default="https://www.facebook.com/GRUPOLIAS")
    Imagen_Telefono_1 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Telefono_1 = models.CharField(max_length=16, blank=False, null=False, default="")
    Link_a_Telefono_1 = models.CharField(max_length=13, blank=False, null=False, default="4434714356")
    Imagen_Telefono_2 = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Telefono_2 = models.CharField(max_length=16, blank=False, null=False, default="")
    Link_a_Telefono_2 = models.CharField(max_length=13, blank=False, null=False, default="+525548335729")
    Correo_electronico_img = models.ForeignKey(
        "wagtailimages.Image",
        null= True,
        blank= False,
        on_delete=models.SET_NULL,
        related_name="+"
    )
    Correo_electronico = models.CharField(max_length=35, blank=False, null=False, default="")
    Url_Maps = models.CharField(max_length=500, blank=False, null=False, default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3756.8164504686365!2d-101.19980278513917!3d19.677834686745502!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x842d0d305391c24b%3A0x40f2a314c0cf0326!2sGRUPO%20LIAS!5e0!3m2!1ses!2smx!4v1650404689145!5m2!1ses!2smx", help_text="Esta URL se consigue en google maps en la etiqueta compartir y en la pestaña 'Incorporar un mapa', se copia todo el link que está en el apartado 'src=' sin las comillas")

    content_panels = Page.content_panels + [
        MultiFieldPanel(
            [ImageChooserPanel("Imagen_Red_Social_1"), 
            FieldPanel("Usuario_Red_Social_1"),
            FieldPanel("Link_a_Red_Social_1"),
            ImageChooserPanel("Imagen_Red_Social_2"),
            FieldPanel("Usuario_Red_Social_2"),
            FieldPanel("Link_a_Red_Social_2"),
            
            ],
            heading="Seccion 1",
        ),
        
        MultiFieldPanel(
            [ImageChooserPanel("Imagen_Telefono_1"), 
            FieldPanel("Telefono_1"),
            FieldPanel("Link_a_Telefono_1"),
            ImageChooserPanel("Imagen_Telefono_2"),
            FieldPanel("Telefono_2"),
            FieldPanel("Link_a_Telefono_2"),
            ],
            heading="Seccion 2",
        ),
        
        MultiFieldPanel(
            [ImageChooserPanel("Correo_electronico_img"), 
            FieldPanel("Correo_electronico"),
            ],
            heading="Seccion 3",
        ),
        FieldPanel("Url_Maps"),
    ]
    
class PreguntasPage(Page):
    max_count=1

    subpage_types = []

    Título_principal = models.CharField(max_length=30, blank=False, null=False, default="")

    content_panels = Page.content_panels + [
        FieldPanel("Título_principal"),
        MultiFieldPanel(
            [InlinePanel("cat_preguntas", max_num=100, min_num=1, label="Pregunta")],
            heading="Preguntas",
        ),
    ]
    
    
    # def get_context(self, request):
    #     context = super().get_context(request)
    #     context['categories'] = PreguntasCategory.objects.all()
    #     return context


class PlantPregunta(Orderable):
    id = models.AutoField(primary_key=True)
    page = ParentalKey(PreguntasPage, on_delete=models.CASCADE, related_name='cat_preguntas')
    pregunta = models.CharField(max_length=100, blank=False, null=False, default="") 
    respuesta = models.CharField(max_length=200, blank=False, null=False, default="")
    # categoría = models.CharField(max_length=40, blank=False, null= False, default="")

    panels = [
        FieldPanel("pregunta"),
        FieldPanel("respuesta"),
        # FieldPanel("categoría"),
    ]
        
class FormField(AbstractFormField):
    id = models.AutoField(primary_key=True)
    page = ParentalKey('CommentPage', on_delete = models.CASCADE, related_name = 'form_fields')
    
    
class CommentPage(AbstractEmailForm):
    max_count=1

    template = "home/comment_form.html"

    subpage_types = []

    Text_EComments=models.TextField(blank=False, null=False,default="")
    Image_EComments=models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = "+"
    )
    
    Texto_de_agradecimiento = RichTextField(blank = True)

    content_panels = AbstractEmailForm.content_panels + [
        ImageChooserPanel("Imagen_de_comentarios"),
        MultiFieldPanel([
            ImageChooserPanel("Image_EComments"),
            FieldPanel("Text_EComments"),
            ],
            heading="Enviar comentarios"
        ),
        InlinePanel ('form_fields', label = 'Form Fields'),
        FieldPanel('Texto_de_agradecimiento'),
    ]

    Imagen_de_comentarios = models.ForeignKey(
        "wagtailimages.Image",
        null = True,
        blank = False,
        on_delete = models.SET_NULL,
        related_name = "+"
    )

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        # If you need to show results only on landing page,
        # you may need check request.method

        results = []
        # Get information about form fields
        data_fields = [
            (field.clean_name, field.label)
            for field in self.get_form_fields()
        ]

        # Get all submissions for current page
        submissions = self.get_submission_class().objects.all()
        for submission in submissions:
            data = submission.get_data()
            results.append(data)

        context.update({
            'results': results,
        })
        print(context)
        return context