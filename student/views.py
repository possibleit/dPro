from django.shortcuts import render,redirect
from .forms import FileUploadForm,FileUploadModelForm
from .models import File,Student,OneClass
from django.http import JsonResponse,HttpResponse,FileResponse,Http404
from django.template.defaultfilters import filesizeformat
from dPro.settings import BASE_DIR
import uuid,os,xlrd,xlwt
from .util import wite_to_excel,import_s
# Create your views here.
# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    return render(request, 'file_list.html', {'files': files})


'''
@Author : Qian
@Date : 15:42 2019/6/10
@Description : 上传文件并导入数据库，方法是先保存文件到/media/files/文件夹下，然后读取保存数据库中
    通过upload1方法导入(file_upload),因为保存文件时文件名保存为一个uuid值，使用model方法和ajax方
    法保存文件后无法获取文件名。
'''
def file_upload(request):
    if request.method == "POST":
        method = request.POST.get('upload_method')
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # get cleaned data
            upload_method = form.cleaned_data.get("upload_method")
            raw_file = form.cleaned_data.get("file")
            new_file = File()
            new_file.file= handle_uploaded_file(raw_file,method)
            new_file.upload_method = upload_method
            new_file.save()
            return redirect("/student/")
    else:
        form = FileUploadForm()

    return render(request, 'upload_form.html', {'form': form,
                                                            'heading': 'Upload files with Regular Form'})


def handle_uploaded_file(file,method):
    print(type(file))
    ext = file.name.split('.')[-1]
    file_name = '{}.{}'.format(uuid.uuid4().hex[:10], ext)
    # file path relative to 'media' folder
    file_path = os.path.join('files', file_name)
    absolute_file_path = os.path.join('media', 'files', file_name)

    directory = os.path.dirname(absolute_file_path)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(absolute_file_path, 'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)
    import_s(absolute_file_path)
    return file_path

def model_form_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("/student/")
    else:
        form = FileUploadModelForm()

    return render(request, 'upload_form.html', {'form': form,
                                                            'heading': 'Upload files with ModelForm'})
def ajax_form_upload(request):
    form = FileUploadModelForm()
    return render(request, 'ajax_upload_form.html', {'form': form,
                                                            'heading': 'File Upload with AJAX'})

# handling AJAX requests
def ajax_upload(request):
    if request.method == "POST":
        form = FileUploadModelForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            # Obtain the latest file list
            files = File.objects.all().order_by('-id')
            data = []
            for file in files:
                data.append({
                    "url": file.file.url,
                    "size": filesizeformat(file.file.size),
                    "upload_method": file.upload_method,
                    })
            return JsonResponse(data, safe=False)
        else:
            data = {'error_msg': "Only jpg, pdf and xlsx files are allowed."}
            return JsonResponse(data)
    return JsonResponse({'error_msg': 'only POST method accpeted.'})
'''
@Author : Qian
@Date : 15:46 2019/6/10
@Description : 导出Student表，excel文件头格式使用util.py/excel_head_style方法定义，内容格式
    使用util/excel_record_style方法定义
'''
def export_preview(request):
    if request.method != 'GET':
        return ("get")
    # 表头字段
    head_data = ['name','sex','age','nativeplace','unitwork','business',
                    'address','resume','email','tel_number','clazz']
    # 查询记录数据
    records = []
    data = Student.objects.filter()
    n = len(data)
    # print(n)
    for item in data:
        if item != "":

            name = item.name
            sex = item.sex
            age = item.age
            nativeplace = item.nativeplace
            unitwork = item.unitwork
            business = item.business
            address = item.address
            resume = item.resume
            email = item.email
            tel_number = item.tel_number
            clazz = item.clazz

            record = []
            record.append(name)
            record.append(sex)
            record.append(str(age))
            record.append(nativeplace)
            record.append(unitwork)
            record.append(business)
            record.append(address)
            record.append(resume)
            record.append(email)
            record.append(str(tel_number))
            record.append(clazz.name)
            # print(record)
        records.append(record)

    ret = wite_to_excel(n, head_data, records)
    file_path = os.path.join(BASE_DIR,ret+'.xls')

    try:
        response = FileResponse(open(file_path, 'rb'))
        response['content_type'] = "application/octet-stream"
        response['Content-Disposition'] = 'attachment; filename=' + os.path.basename(file_path)
        print(os.path.basename(file_path))
        return response
    except Exception:
        raise Http404