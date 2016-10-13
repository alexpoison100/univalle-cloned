from django.shortcuts import render
from django.template import RequestContext
from univalle.home.forms import ContactForm, LoginForm, RegisterForm
from django.core.mail import EmailMultiAlternatives #Enviamos html
from django.contrib.auth import login, logout, authenticate 
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage#paginacion de Django
from django.contrib.auth.models import User

# creamos nuestras vistas

def index_view(request):
	#muestra el index pero con el formulario de contacto
	info_enviado = False #definir si se envio la info
	nombre = ""
	correo = ""
	asunto = ""
	mensaje = ""
	if request.method == "POST":
		formulario = ContactForm(request.POST)
		if formulario.is_valid():
			info_enviado = True
			nombre = formulario.cleaned_data['Nombre']
			correo = formulario.cleaned_data['Correo']
			asunto = formulario.cleaned_data['Asunto']
			mensaje = formulario.cleaned_data['Mensaje']

			#configuracion enviando mensaje via gmail
			to_admin = 'alexpoison100@gmail.com'
			html_content ="<b>Informacion recibida de:</b> %s <br><b>Asunto:</b> %s<br><br><b>***Mensaje***</b><br><br>%s"%(correo,asunto,mensaje)
			msg = EmailMultiAlternatives("Correo de Contacto",html_content,'from@server.com',[to_admin])
			msg.attach_alternative(html_content,'text/html')#definimos el contenido como HTML
			msg.send()#Enviamos el correo
	else:
		formulario = ContactForm()
	ctx = {'form':formulario,'nombre':nombre,'correo':correo,'asunto':asunto,'mensaje':mensaje,'info_enviado':info_enviado}
	return render(request,'index.html',ctx)

def about_view(request):
	mensaje ="Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render(request,'about.html',ctx)



def login_view(request):
	mensaje=""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')#lo direccionamos a la raiz si esta autenticado
	else:
		if request.method == "POST":
			form = LoginForm(request.POST)
			if form.is_valid():
				username = form.cleaned_data['Usuario']
				password = form.cleaned_data['Contrasena']
				usuario = authenticate(username=username,password=password)
				if usuario is not None and usuario.is_active:
					login(request,usuario)
					return HttpResponseRedirect('/')
				else:
					mensaje="Usuario y/o password incorrecto"
		form = LoginForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render(request,'login.html',ctx)
	 
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	form = RegisterForm()
	if request.method == "POST":
		form = RegisterForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			email = form.cleaned_data['email']
			password_one = form.cleaned_data['password_one']
			password_two = form.cleaned_data['password_two']
			u = User.objects.create_user(username=username, email=email, password=password_one)
			u.save()#guarda el usuario
			return render(request,'thanks_register.html')
		else:
			ctx = {'form':form}
			return render(request,'registro.html',ctx)

	ctx	= {'form':form}
	return render(request,'registro.html', ctx)
	