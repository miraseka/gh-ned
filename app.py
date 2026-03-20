from flask import Flask, request, send_file
from docxtpl import DocxTemplate
import os
import io

app = Flask(__name__)

# Сопоставление типа организации с файлом шаблона
TEMPLATES = {
    "ТОО": "договор типовой ТОО.docx",
    "ИП": "договор типовой ИП.docx",
    "ФИЗЛИЦО": "договор типовой Физ лицо.docx"
}

@app.route('/generate', methods=['POST'])
def generate_contract():
    data = request.form.to_dict()
    org_type = data.get('org_type')
    
    if org_type not in TEMPLATES:
        return "Ошибка: Неверный тип организации", 400

    template_path = TEMPLATES[org_type]
    
    if not os.path.exists(template_path):
        return f"Ошибка: Файл шаблона {template_path} не найден.", 404

    # Загружаем шаблон
    doc = DocxTemplate(template_path)
    
    # Формируем словарь контекста для заполнения (объединяем все возможные ключи)
    context = {
        "contract_date": data.get("contract_date", ""),
        "contract_amount": data.get("contract_amount", ""),
        "ad_budget": data.get("ad_budget", ""),
        "seo_amount": data.get("seo_amount", ""),
        
        # Поля ТОО
        "director_fio": data.get("director_fio", ""),
        "company_name": data.get("company_name", ""),
        "address": data.get("address", ""),
        "bin": data.get("bin", ""),
        "bank": data.get("bank", ""),
        "kbe": data.get("kbe", ""),
        "bik": data.get("bik", ""),
        "account_number": data.get("account_number", ""),
        
        # Поля ИП
        "ip_company_name": data.get("ip_company_name", ""),
        "ip_address": data.get("ip_address", ""),
        "ip_iin": data.get("ip_iin", ""),
        "ip_bank": data.get("ip_bank", ""),
        "ip_kbe": data.get("ip_kbe", ""),
        "ip_bik": data.get("ip_bik", ""),
        "ip_account_number": data.get("ip_account_number", ""),
        
        # Поля Физлица
        "fiz_fio": data.get("fiz_fio", ""),
        "fiz_address": data.get("fiz_address", ""),
        "fiz_phone": data.get("fiz_phone", ""),
        "fiz_iin": data.get("fiz_iin", "")
    }

    # Заполняем документ данными
    doc.render(context)
    
    # Сохраняем во временный буфер в оперативной памяти
    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)
    
    # Отправляем файл пользователю для скачивания 
    filename = f"Договор_{org_type}_{context['contract_date']}.docx"
    return send_file(
        file_stream, 
        as_attachment=True, 
        download_name=filename,
        mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    )

if __name__ == '__main__':
    # Запуск сервера
    app.run(debug=True, port=5000)
