from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from apps.accounts.models import Empresa, Profesional, Usuario
from apps.jobs.models import JobOffer
from apps.network.models import ConnectionRequest
from apps.posts.models import Publication


class Command(BaseCommand):
    PROFESSIONAL_NAMES = [
        ("Camila", "Rojas"),
        ("Nicolás", "Salvatierra"),
        ("María", "Fernández"),
        ("Sofía", "Mendoza"),
        ("Diego", "López"),
        ("Valentina", "Quiroga"),
        ("Andrés", "Paredes"),
        ("Paola", "Vargas"),
        ("Joaquín", "Montaño"),
        ("Lucía", "Peña"),
    ]

    COMPANY_PROFILES = [
        {
            "name": "AndesTech Solutions",
            "industry": "desarrollo de software",
            "description": "Consultora de productos digitales para pymes y sector educativo.",
        },
        {
            "name": "Logistica Norte",
            "industry": "logistica y cadena de suministro",
            "description": "Operador logistica para retail y ecommerce en todo el pais.",
        },
        {
            "name": "Clinica Santa Lucia",
            "industry": "salud privada",
            "description": "Centro medico con servicios ambulatorios y telemedicina.",
        },
        {
            "name": "Finanzas Delta",
            "industry": "servicios financieros",
            "description": "Firma de analisis financiero y automatizacion contable.",
        },
        {
            "name": "EcoEnergia LATAM",
            "industry": "energia renovable",
            "description": "Empresa de proyectos solares para industria y comercio.",
        },
        {
            "name": "AgroVision",
            "industry": "tecnologia agricola",
            "description": "Plataforma de monitoreo de cultivos y eficiencia hidrica.",
        },
        {
            "name": "EducaNet",
            "industry": "edtech",
            "description": "Soluciones de aprendizaje en linea para institutos tecnicos.",
        },
        {
            "name": "Constructora Horizonte",
            "industry": "construccion",
            "description": "Desarrollo de proyectos habitacionales y obras civiles.",
        },
    ]

    PROFESSIONAL_POST_TEMPLATES = [
        "Hoy cerramos el sprint del modulo de autenticacion. Reducimos tiempos de carga y mejoramos trazabilidad de errores.",
        "Comparto aprendizajes de una integracion con APIs externas: contratos claros, timeouts y monitoreo desde el primer dia.",
        "En la semana nos enfocamos en pruebas automatizadas. Pasamos de cobertura parcial a un flujo mas confiable para deploy.",
        "Terminamos una mejora de UX en onboarding. Menos friccion en registro y mejor conversion en los primeros pasos.",
        "Documentar bien tambien es productividad. Actualizamos guias internas y bajamos consultas repetidas del equipo.",
        "Probamos una estrategia de caché para reportes y el tiempo de respuesta bajo de forma notable en horas pico.",
    ]

    COMPANY_POST_TEMPLATES = [
        "Estamos expandiendo operaciones y buscamos perfiles con enfoque colaborativo para proyectos de alto impacto.",
        "Compartimos avance del trimestre: mejoramos indicadores de servicio y abrimos nuevas iniciativas de innovacion.",
        "Nuestro equipo implemento mejoras de procesos que reducen retrabajo y elevan la calidad de entrega.",
        "Abrimos programa de practicas para talento junior con mentoria y plan de crecimiento por competencias.",
        "Seguimos fortaleciendo cultura de trabajo flexible, aprendizaje continuo y resultados medibles.",
        "Estamos cerrando alianzas estrategicas para ampliar cobertura y acelerar implementaciones en clientes.",
    ]

    JOB_TEMPLATES = [
        {
            "title": "Desarrollador Backend Python",
            "description": "Participarás en el diseño de APIs, integraciones y optimización de rendimiento para productos internos de la compañía.",
            "location": "Remoto",
            "salary_range": "$1,400 - $2,000",
        },
        {
            "title": "Analista de Datos",
            "description": "Apoyarás la toma de decisiones del negocio con tableros, limpieza de datos y análisis de tendencias de desempeño.",
            "location": "Híbrido - La Paz",
            "salary_range": "$1,100 - $1,600",
        },
        {
            "title": "Especialista de Soporte Técnico",
            "description": "Gestionarás incidencias, documentación técnica y mejora continua de la atención al cliente en operación diaria.",
            "location": "Presencial - Santa Cruz",
            "salary_range": "$900 - $1,300",
        },
        {
            "title": "Diseñador UI/UX",
            "description": "Trabajarás con producto y desarrollo para construir experiencias claras, medibles y orientadas a conversión.",
            "location": "Híbrido - Cochabamba",
            "salary_range": "$1,200 - $1,700",
        },
    ]

    help = (
        "Crea datos iniciales: usuarios, publicaciones, ofertas laborales y "
        "conexiones aceptadas entre usuarios."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--usuarios-profesionales",
            type=int,
            default=8,
            help="Cantidad de usuarios tipo profesional.",
        )
        parser.add_argument(
            "--usuarios-empresa",
            type=int,
            default=3,
            help="Cantidad de usuarios tipo empresa.",
        )
        parser.add_argument(
            "--publicaciones-por-usuario",
            type=int,
            default=2,
            help="Cantidad de publicaciones por usuario.",
        )
        parser.add_argument(
            "--ofertas-por-empresa",
            type=int,
            default=2,
            help="Cantidad de ofertas por cada empresa.",
        )
        parser.add_argument(
            "--password",
            type=str,
            default="SocialIT12345",
            help="Contraseña para todos los usuarios de datos iniciales.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        total_profesionales = max(0, options["usuarios_profesionales"])
        total_empresas = max(0, options["usuarios_empresa"])
        publicaciones_por_usuario = max(0, options["publicaciones_por_usuario"])
        ofertas_por_empresa = max(0, options["ofertas_por_empresa"])
        password = options["password"]

        self._cleanup_legacy_seed_users()

        professionals = self._crear_profesionales(total_profesionales, password)
        companies = self._crear_empresas(total_empresas, password)

        all_users = professionals + companies
        self._reset_seed_content(all_users, companies)
        publications_created = self._crear_publicaciones(
            all_users,
            publicaciones_por_usuario,
        )
        offers_created = self._crear_ofertas(companies, ofertas_por_empresa)
        accepted_connections = self._crear_conexiones_aceptadas(all_users)

        self.stdout.write(self.style.SUCCESS("Datos iniciales generados correctamente."))
        self.stdout.write(f"- Usuarios profesionales: {len(professionals)}")
        self.stdout.write(f"- Usuarios empresa: {len(companies)}")
        self.stdout.write(f"- Publicaciones creadas: {publications_created}")
        self.stdout.write(f"- Ofertas creadas: {offers_created}")
        self.stdout.write(f"- Conexiones aceptadas: {accepted_connections}")
        self.stdout.write("Prefijos de usuario creados: profesional_ y empresa_")

    def _cleanup_legacy_seed_users(self):
        User = get_user_model()
        legacy_users = User.objects.filter(
            Q(username__startswith='demo_prof_') |
            Q(username__startswith='demo_emp_')
        )
        if legacy_users.exists():
            legacy_users.delete()

    def _crear_profesionales(self, cantidad, password):
        users = []
        for i in range(1, cantidad + 1):
            first_name, last_name = self.PROFESSIONAL_NAMES[(i - 1) % len(self.PROFESSIONAL_NAMES)]
            username = f"profesional_{i}"
            email = f"{first_name.lower()}.{last_name.lower()}{i}@socialit.com"

            user = self._get_or_create_user(
                username=username,
                email=email,
                password=password,
                tipo=Usuario.TipoUsuario.PROFESIONAL,
                first_name=first_name,
                last_name=last_name,
                nombre_mostrado=f"{first_name} {last_name}",
            )

            Profesional.objects.update_or_create(
                usuario=user,
                defaults={
                    "nombre": first_name,
                    "apellido": last_name,
                    "experienciaLaboral": "Experiencia en proyectos web, integración de APIs y mejora de procesos digitales.",
                    "certificaciones": "Certificación en desarrollo de software y metodologías ágiles.",
                },
            )
            users.append(user)
        return users

    def _crear_empresas(self, cantidad, password):
        users = []
        for i in range(1, cantidad + 1):
            company_profile = self.COMPANY_PROFILES[(i - 1) % len(self.COMPANY_PROFILES)]
            username = f"empresa_{i}"
            email = f"contacto{i}@socialit.com"
            razon_social = company_profile["name"]

            user = self._get_or_create_user(
                username=username,
                email=email,
                password=password,
                tipo=Usuario.TipoUsuario.EMPRESA,
                first_name="",
                last_name="",
                nombre_mostrado=razon_social,
            )

            Empresa.objects.update_or_create(
                usuario=user,
                defaults={
                    "razonSocial": razon_social,
                    "infoEmpresa": (
                        f"Empresa del rubro {company_profile['industry']}. "
                        f"{company_profile['description']}"
                    ),
                },
            )
            users.append(user)
        return users

    def _reset_seed_content(self, users, companies):
        # Reemplaza contenido previo para mantener el dataset consistente.
        Publication.objects.filter(author__in=users).delete()
        JobOffer.objects.filter(created_by__in=companies).delete()

    def _get_or_create_user(
        self,
        username,
        email,
        password,
        tipo,
        first_name,
        last_name,
        nombre_mostrado,
    ):
        User = get_user_model()
        user, created = User.objects.get_or_create(
            username=username,
            defaults={
                "email": email,
                "first_name": first_name,
                "last_name": last_name,
                "tipoUsuario": tipo,
                "nombreMostrado": nombre_mostrado,
                "is_active": True,
            },
        )

        updated_fields = []
        if user.email != email:
            user.email = email
            updated_fields.append("email")
        if user.first_name != first_name:
            user.first_name = first_name
            updated_fields.append("first_name")
        if user.last_name != last_name:
            user.last_name = last_name
            updated_fields.append("last_name")
        if user.tipoUsuario != tipo:
            user.tipoUsuario = tipo
            updated_fields.append("tipoUsuario")
        if user.nombreMostrado != nombre_mostrado:
            user.nombreMostrado = nombre_mostrado
            updated_fields.append("nombreMostrado")
        if not user.is_active:
            user.is_active = True
            updated_fields.append("is_active")

        if created or not user.check_password(password):
            user.set_password(password)
            updated_fields.append("password")

        if updated_fields:
            user.save(update_fields=updated_fields)

        return user

    def _crear_publicaciones(self, users, por_usuario):
        created_count = 0
        if por_usuario == 0:
            return created_count

        for user in users:
            for i in range(1, por_usuario + 1):
                if user.tipoUsuario == Usuario.TipoUsuario.EMPRESA:
                    base_templates = self.COMPANY_POST_TEMPLATES
                    context_text = (
                        f"Empresa: {user.nombreMostrado or user.username}."
                    )
                else:
                    base_templates = self.PROFESSIONAL_POST_TEMPLATES
                    context_text = f"Autor: {user.nombreMostrado or user.username}."

                template_text = base_templates[(i - 1) % len(base_templates)]
                content = f"{template_text} {context_text}"
                _, created = Publication.objects.get_or_create(
                    author=user,
                    content=content,
                )
                if created:
                    created_count += 1
        return created_count

    def _crear_ofertas(self, companies, por_empresa):
        created_count = 0
        if por_empresa == 0:
            return created_count

        for company_user in companies:
            company_label = company_user.nombreMostrado or company_user.username
            for i in range(1, por_empresa + 1):
                job_template = self.JOB_TEMPLATES[(i - 1) % len(self.JOB_TEMPLATES)]
                title = f"{job_template['title']} - {company_label}"
                _, created = JobOffer.objects.get_or_create(
                    created_by=company_user,
                    company_name=company_label,
                    title=title,
                    defaults={
                        "description": job_template["description"],
                        "location": job_template["location"],
                        "salary_range": job_template["salary_range"],
                    },
                )
                if created:
                    created_count += 1
        return created_count

    def _crear_conexiones_aceptadas(self, users):
        if len(users) < 2:
            return 0

        created_or_updated = 0

        for idx in range(len(users)):
            sender = users[idx]
            receiver = users[(idx + 1) % len(users)]
            if sender.pk == receiver.pk:
                continue

            pair_qs = ConnectionRequest.objects.filter(
                sender__in=[sender, receiver],
                receiver__in=[sender, receiver],
            )

            relation = pair_qs.first()
            if relation is None:
                ConnectionRequest.objects.create(
                    sender=sender,
                    receiver=receiver,
                    status=ConnectionRequest.Status.ACCEPTED,
                )
                created_or_updated += 1
                continue

            if relation.status != ConnectionRequest.Status.ACCEPTED:
                relation.status = ConnectionRequest.Status.ACCEPTED
                relation.save(update_fields=["status", "updated_at"])
                created_or_updated += 1

        return created_or_updated
