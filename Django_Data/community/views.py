from django.shortcuts import render, redirect
from community.forms import *
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def write(request):
	if request.method == "POST":
		form = Form(request.POST, request.FILES)
		if form.is_valid():
			print("saved!")
			form.save()  # form을 그대로 db에 저장(자동으로!)
			return redirect('list')
	else:
		form = Form()
		print("call form!")
		
	return render(request, 'write.html',{'form':form})

def list(request):
	articleList = Article.objects.all()
	return render(request, 'list.html',{'articleList':articleList})

@csrf_exempt
def upload(request):
	if request.method == "POST":
		form = Form(request.POST, request.FILES)
		if form.is_valid():
			print("valid")
			form.save()  # form을 그대로 db에 저장(자동으로!)
			return redirect('list')
	else:
		form = Form()
	
	
	
def view(request, num="1"):
	#article = Article(request.FILES, id=num)
	article = Article.objects.get(id = num)

	return render(request, 'view.html', {'article':article})
	#article = Article.objects.get(id=num)
	#article.img = request.FILES['img']
	#return render(request, 'view.html',{'article':article})

#def img(request, num="1"):
#    article = Article.objects.get(id = num)
#    return render(request, 'img.html',{'article':article})