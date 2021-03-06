# -*- coding: utf-8 -*- 
from django.shortcuts import render
from django.template import RequestContext
from univalle.home.forms import *
from univalle.home.models import *
from django.core.mail import EmailMultiAlternatives #Enviamos html
from django.contrib.auth import login, logout, authenticate 
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator, EmptyPage, InvalidPage#paginacion de Django
from django.contrib.auth.models import User
import itertools#contador indice de la tabla
import requests
import simplejson
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
	ctx = {'form':formulario,'info_enviado':info_enviado}
	return render(request,'index.html',ctx)

def about_view(request):
	mensaje ="Esto es un mensaje desde mi vista"
	ctx = {'msg':mensaje}
	return render(request,'about.html',ctx)

def info_carreras_view(request):
	mensaje=""
	#datos de ingenieria en sistemas
	try:
		s= programasAcademico.objects.get(codigo=3743)
	except programasAcademico.DoesNotExist:
		mensaje="No existe programa"
	else:
		nombre_sistemas= s.nombre
		puntaje_sistemas= s.puntaje_min
		cupos_sistemas=s.cupos
		info_sistemas= s.info
	#datos de tecnologia en sistemas	
	try:
		s= programasAcademico.objects.get(codigo=2711)
	except programasAcademico.DoesNotExist:
		mensaje="No existe programa"
	else:
		nombre_tecsistemas= s.nombre
		puntaje_tecsistemas= s.puntaje_min
		cupos_tecsistemas=s.cupos
		info_tecsistemas= s.info
		#datos de ingenieria en quimica
	try:
		s= programasAcademico.objects.get(codigo=3749)
	except programasAcademico.DoesNotExist:
		mensaje="No existe programa"
	else:
		nombre_quimica= s.nombre
		puntaje_quimica= s.puntaje_min
		cupos_quimica=s.cupos
		info_quimica= s.info
	#datos de tecnologia en quimica	
	try:
		s= programasAcademico.objects.get(codigo=2131)
	except programasAcademico.DoesNotExist:
		mensaje="No existe programa"
	else:
		nombre_tecquimica= s.nombre
		puntaje_tecquimica= s.puntaje_min
		cupos_tecquimica=s.cupos
		info_tecquimica= s.info
	#datos de ingenieria en electronica
	try:
		s= programasAcademico.objects.get(codigo=3744)
	except programasAcademico.DoesNotExist:
		mensaje="No existe programa"
	else:
		nombre_electronica= s.nombre
		puntaje_electronica= s.puntaje_min
		cupos_electronica=s.cupos
		info_electronica= s.info
	#datos de tecnologia en electronica	
	try:
		s= programasAcademico.objects.get(codigo=2710)
	except programasAcademico.DoesNotExist:
		mensaje="No existe programa"
	else:
		nombre_tecelectronica= s.nombre
		puntaje_tecelectronica= s.puntaje_min
		cupos_tecelectronica=s.cupos
		info_tecelectronica= s.info
		
	ctx = {'nombre_sistemas':nombre_sistemas,'puntaje_sistemas':puntaje_sistemas,'cupos_sistemas':cupos_sistemas,'info_sistemas':info_sistemas,
		'nombre_tecsistemas':nombre_tecsistemas,'puntaje_tecsistemas':puntaje_tecsistemas,'cupos_tecsistemas':cupos_tecsistemas,'info_tecsistemas':info_tecsistemas,
		'nombre_quimica':nombre_quimica,'puntaje_quimica':puntaje_quimica,'cupos_quimica':cupos_quimica,'info_quimica':info_quimica,
		'nombre_tecquimica':nombre_tecquimica,'puntaje_tecquimica':puntaje_tecquimica,'cupos_tecquimica':cupos_tecquimica,'info_tecquimica':info_tecquimica,
		'nombre_electronica':nombre_electronica,'puntaje_electronica':puntaje_electronica,'cupos_electronica':cupos_electronica,'info_electronica':info_electronica,
		'nombre_tecelectronica':nombre_tecelectronica,'puntaje_tecelectronica':puntaje_tecelectronica,'cupos_tecelectronica':cupos_tecelectronica,'info_tecelectronica':info_tecelectronica,
	}
	return render(request,'info_carreras.html',ctx)

def login_view(request):
	mensaje=""
	if request.user.is_authenticated():
		return HttpResponseRedirect('/')#lo direccionamos a la raiz si no esta autenticado
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
			else:
					mensaje="Falta llenar campos vacios"
		form = LoginForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render(request,'login.html',ctx)
	 
def logout_view(request):
	logout(request)
	return HttpResponseRedirect('/')

def register_view(request):
	info="inicializado"
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
			info = "Datos incorrectos"
			ctx = {'form':form,'info':info}
			return render(request,'registro.html',ctx)

	ctx	= {'form':form}
	return render(request,'registro.html', ctx)
	
def resultados_view(request):
	if request.user.is_authenticated():
		mensaje =""
		programas_academicos=""
		form = ResultadoForm()
		
		if request.method == "POST":
			form = ResultadoForm(request.POST)
			
			if form.is_valid():
				programas_academicos = str(form.cleaned_data['programas_academicos'])
				form = ResultadoForm(request.POST)
				return HttpResponseRedirect('/listar_admitidos/pagina/1/programa/%s' % programas_academicos)
			else:
				mensaje = "No ha seleccionado ninguna Carrera"
				ctx = {'form':form}
				return render(request,'resultados.html',ctx)
		form = ResultadoForm()
		ctx = {'form':form, 'mensaje':mensaje}
		return render(request,'resultados.html',ctx)
	else:
		return HttpResponseRedirect('/login')
		
def add_inscripciones_view(request):
	if request.user.is_authenticated():
		if request.method == "POST":
			formulario = InscripcionesForm(request.POST)
			info = "Inicializando"
			
			if formulario.is_valid():
				cedula = formulario.cleaned_data['cedula']
				nombre = formulario.cleaned_data['nombre']
				apellido = formulario.cleaned_data['apellido']
				snp = formulario.cleaned_data['snp']
				if snp:
					icfes = requests.get('https://morning-brushlands-79611.herokuapp.com/v1/resultados/?codigo=%s&format=json' % snp)
					icfes_json = icfes.json()
					lectura_critica= (icfes_json[0]["lectura_critica"])
					matematicas= (icfes_json[0]["matematicas"])
					sociales= (icfes_json[0]["sociales"])
					naturales= (icfes_json[0]["naturales"])
					ingles= (icfes_json[0]["ingles"])
					razonamiento_cuantitativo= (icfes_json[0]["razonamiento_cuantitativo"])
					competencias_ciudadanas= (icfes_json[0]["competencias_ciudadanas"])
				colegio = formulario.cleaned_data['colegio']
				ref_pago = formulario.cleaned_data['ref_pago']
				if ref_pago:
					respuesta = requests.get('http://ws-bank-julianrico.c9users.io/rest/consignacion/?cedula=%s&format=json' % ref_pago)
					respuesta_json = respuesta.json()
				programa = str(formulario.cleaned_data['programas_academicos'])
			
				i = inscripciones() #creo una instancia de la clase inscripcion
				
				i.cedula = cedula
				i.nombre = nombre
				i.apellido = apellido
				i.snp = snp
				i.lectura_critica = lectura_critica
				i.matematicas = matematicas
				i.sociales = sociales
				i.naturales = naturales
				i.ingles = ingles
				i.razonamiento_cuantitativo = razonamiento_cuantitativo
				i.competencias_ciudadanas = competencias_ciudadanas
				i.colegio = colegio
				i.ref_pago = ref_pago
				i.carrera = programa
				
				i.save() #guardar inscripcion
				
				#Consulta de los ponderados de cada materia
				try:
					p = programasAcademico.objects.get(nombre=programa)
				except programasAcademico.DoesNotExist:
					info = "Programa No existe"
				else:
					pl = p.lectura_critica
					pm = p.matematicas
					ps = p.sociales
					pn = p.naturales
					pi = p.ingles
					pr = p.razonamiento_cuantitativo
					pc = p.competencias_ciudadanas
				#Aqui se multiplica cada uno de los resultados de cada prueba por la ponderación que el programa académico 
				puntaje = float((lectura_critica) * (pl)) + float((matematicas) * (pm)) + float((sociales) * (ps)) + float((naturales) * (pn)) + float((ingles) * (pi)) + float((razonamiento_cuantitativo) * (pr)) + float((competencias_ciudadanas) * (pc))
				
				#Guardo datos para generar la lista de admitidos
				a = lista_admitidos() #creo una instancia de la clase lista
				
				a.cedula = cedula
				a.nombre = nombre
				a.apellido = apellido
				a.puntaje = puntaje                         
				a.carrera = programa
				
				a.save() #guardar listado
				info = "Inscripción Satisfactoria!!!!!!"
				formulario = InscripcionesForm()
			else:
				info = "Informacion con datos incorrectos"
			form = InscripcionesForm()
			ctx = {'form':formulario, 'informacion':info}
			return render(request,'inscripciones.html',ctx)

		else:
			formulario = InscripcionesForm()
		ctx = {'form':formulario}
		return render(request,'inscripciones.html',ctx)
	else:
		return HttpResponseRedirect('/')

def listar_admitidos_view(request,pagina,carrera=None):
	iterator = itertools.count(1)#me genera un contador para el indice de la tabla
	if request.user.is_authenticated():
	#Consulta de cantidad de cupos segun el programa academico 
		try:
			p = programasAcademico.objects.get(nombre=carrera)
		except programasAcademico.DoesNotExist:
			info = "Programa No existe"
		else:
			cupos = p.cupos
	#Metodo  para listar inscripciones
		#consulta por carrera, de mayor a menor puntaje y seleccionado una cantidad de cupo
		list_admitidos = lista_admitidos.objects.filter(carrera=carrera).order_by('-puntaje')[:cupos]
		paginator = Paginator(list_admitidos,20)
		try:
			page = int(pagina)
		except:
			page = 1
		try:
			admitidos = paginator.page(page)
		except:
			admitidos = paginator.page(paginator.num_pages)
			
		ctx = {'admitidos':admitidos,'iterator':iterator,'carrera':carrera}
		return render(request, 'listar_admitidos.html',ctx)
	else:
		return HttpResponseRedirect('/login')	
		
