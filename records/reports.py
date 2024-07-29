from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import HistorialMedico
import json
import os
import logging
import io
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from PyPDF2 import PdfReader, PdfWriter
from .models import HistorialMedico, RevisionOrganosSistemas, ExamenFisico
import textwrap

logger = logging.getLogger(__name__)

@csrf_exempt
def generar_pdf_historial(request, id_historial):
    if request.method == 'POST':
        data = json.loads(request.body)
        pages = data.get('pages', [])
        logger.debug(f"Generando PDF para historial {id_historial}")
        logger.debug(f"Páginas solicitadas: {pages}")

        historial = get_object_or_404(HistorialMedico, id_historial=id_historial)
        template_path = os.path.join(settings.BASE_DIR, 'records/templates/Historial.pdf')
        template_pdf = PdfReader(template_path)

        output_pdf = PdfWriter()
        num_template_pages = len(template_pdf.pages)
        logger.debug(f"Template PDF tiene {num_template_pages} páginas")

        for page_num in pages:
            try:
                page_index = int(page_num) - 1
                if page_index < 0 or page_index >= num_template_pages:
                    logger.warning(f"Índice de página {page_index} fuera de rango")
                    continue  # Skip invalid page numbers

                template_page = template_pdf.pages[page_index]

                packet = io.BytesIO()
                can = canvas.Canvas(packet, pagesize=letter)

                if page_index == 0:
                    # Ajusta las coordenadas según la estructura del PDF proporcionado
                    can.drawString(110, 735, f"{historial.paciente.name}")
                    can.drawString(450, 734, f"{datetime.now().strftime('%Y-%m-%d')}")
                    can.drawString(164, 706, f"{historial.paciente.identification}")
                    can.drawString(177, 679, f"{historial.paciente.birthdate.strftime('%Y-%m-%d')}")
                    if historial.signos_vitales:
                        can.drawString(154, 591, f"{historial.signos_vitales.temperatura}")
                        can.drawString(425, 591, f"{historial.signos_vitales.frecuencia_cardiaca}")
                        can.drawString(145, 564, f"{historial.signos_vitales.presion_arterial_sistolica}/{historial.signos_vitales.presion_arterial_diastolica}")
                        can.drawString(435, 565, f"{historial.signos_vitales.frecuencia_respiratoria}")
                        can.drawString(115, 537, f"{historial.signos_vitales.peso}")
                        can.drawString(370, 537, f"{historial.signos_vitales.talla}")
                        can.drawString(208, 509, f"{historial.signos_vitales.saturacion_oxigeno}")
                    if historial.consulta:
                        can.drawString(60, 420, f"Motivo de consulta: {historial.consulta.motivo}")
                        can.drawString(60, 300, f"Notas médicas: {historial.consulta.notas_medicas}")

                elif page_index == 1:
                    revisiones = RevisionOrganosSistemas.objects.filter(paciente=historial.paciente)
                    y_position = 720
                    for revision in revisiones:
                        can.drawString(80, y_position, f"{revision.tipo_organos.tipo}: {revision.descripcion}")
                        y_position -= 20

                elif page_index == 2:
                    examenes = ExamenFisico.objects.filter(paciente=historial.paciente)
                    y_position = 720
                    for examen in examenes:
                        can.drawString(80, y_position, f"{examen.tipo_area.tipo_area}: {examen.descripcion}")
                        y_position -= 20

                elif page_index == 3:
                    if historial.diagnostico:
                        can.drawString(80, 730, f"Diagnóstico: {historial.diagnostico.nombre}")
                        can.drawString(80, 680, f"Descripción: {historial.diagnostico.descripcion}")
                    if historial.tratamiento:
                        can.drawString(80, 570, f"Tratamiento: {historial.tratamiento.descripcion}")
                        can.drawString(80, 545, f"Duración: {historial.tratamiento.duracion}")
                        can.drawString(80, 520, f"Dosis: {historial.tratamiento.dosis}")
                        can.drawString(80, 495, f"Frecuencia: {historial.tratamiento.frecuencia}")
                    if historial.receta:
                        can.drawString(80, 420, f"Receta: {historial.receta.medicamentos_recetados}")

                can.save()
                packet.seek(0)
                new_pdf = PdfReader(packet)
                page = template_page
                page.merge_page(new_pdf.pages[0])
                output_pdf.add_page(page)

            except Exception as e:
                logger.error(f"Error al procesar la página {page_num}: {e}")
                continue

        if output_pdf.pages:
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="historial_medico_{id_historial}.pdf"'
            output_pdf.write(response)
            return response
        else:
            return JsonResponse({'error': 'No se pudieron generar páginas válidas'}, status=400)

    return JsonResponse({'error': 'Método no permitido'}, status=405)