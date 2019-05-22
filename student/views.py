from django.shortcuts import render,redirect
from .forms import FileUploadForm,FileUploadModelForm
from .models import File,Student,OneClass
from django.http import JsonResponse
from django.template.defaultfilters import filesizeformat
import uuid,os,xlrd
# Create your views here.
# Show file list
def file_list(request):
    files = File.objects.all().order_by("-id")
    return render(request, 'file_list.html', {'files': files})


# Regular file upload without using ModelForm
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
    data = xlrd.open_workbook(absolute_file_path)
    table = data.sheets()[0]
    print(data.sheet_names())
    nrows = table.nrows
    li = []
    for i in range(1,nrows):
        s = table.row_values(i, start_colx=0, end_colx=None)
        print(s)
        cla = OneClass.objects.get_or_create(name=s[10])[0]
        stu = Student(
            name=s[0],
            sex=s[1],
            age=s[2],
            nativeplace=s[3],
            unitwork=s[4],
            business=s[5],
            address=s[6],
            resume=s[7],
            email=s[8],
            tel_number=s[9],
            clazz=cla,
        )
        li.append(stu)

    Student.objects.bulk_create(li)
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