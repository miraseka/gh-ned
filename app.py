import os
import io
from flask import Flask, render_template, request, send_file
from docxtpl import DocxTemplate

app = Flask(__name__)

TEMPLATES = {
    "ТОО": "договор типовой ТОО.docx",
    "ИП": "договор типовой ИП.docx",
    "ФИЗЛИЦО": "договор типовой Физ лицо.docx"
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_contract():
    data = request.form.to_dict()
    org_type = data.get('org_type')
    
    template_path = TEMPLATES.get(org_type)
    if not template_path or not os.path.exists(template_path):
        return f"Ошибка: Шаблон для {org_type} не найден", 404

    doc = DocxTemplate(template_path)
    
    # Собираем данные из формы
    context = {k: v for k, v in data.items()}
    
    doc.render(context)
    
    target_stream = io.BytesIO()
    doc.save(target_stream)
    target_stream.seek(0)
    
    return send_file(
        target_stream,
        as_attachment=True,
        download_name=f"Contract_{org_type}.docx",
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == '__main__':
    app.run()
