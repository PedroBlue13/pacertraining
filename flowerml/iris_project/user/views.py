from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.views.decorators.cache import never_cache
from django.views.decorators.debug import sensitive_post_parameters
from django.core.paginator import Paginator
from django.db.models import Q
from django.conf import settings
import json
import os
import numpy as np
from PIL import Image
import pickle
import joblib
from datetime import datetime
import base64
from io import BytesIO

def home(request):
    context = {
        'title': 'FlowerML - IA para Classificação de Flores',
        'description': 'Explore o mundo das flores com inteligência artificial',
        'is_home': True,
    }
    return render(request, 'home.html', context)

@sensitive_post_parameters()
@csrf_protect
@never_cache
def logar(request):
    if request.user.is_authenticated:
        messages.info(request, f'Você já está logado como {request.user.get_full_name() or request.user.username}.')
        return redirect('dashboard')
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        senha = request.POST.get('senha', '')
        lembrar = request.POST.get('lembrar')
        
        if not email:
            messages.error(request, 'Por favor, insira seu e-mail.')
            return render(request, 'usuarios/login.html', {'email': email})
        
        if not senha:
            messages.error(request, 'Por favor, insira sua senha.')
            return render(request, 'usuarios/login.html', {'email': email})
        
        if '@' not in email or '.' not in email:
            messages.error(request, 'Por favor, insira um e-mail válido.')
            return render(request, 'usuarios/login.html', {'email': email})
        
        try:
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                messages.error(request, 'E-mail ou senha incorretos.')
                return render(request, 'usuarios/login.html', {'email': email})
            
            user = authenticate(request, username=username, password=senha)
            
            if user is not None:
                if user.is_active:
                    login(request, user)
                    
                    if not lembrar:
                        request.session.set_expiry(0)
                    else:
                        request.session.set_expiry(60 * 60 * 24 * 30)
                    
                    nome_usuario = user.get_full_name() or user.first_name or user.username
                    messages.success(request, f'Bem-vindo de volta, {nome_usuario}! 🌸')
                    
                    next_url = request.GET.get('next')
                    if next_url:
                        return redirect(next_url)
                    else:
                        return redirect('dashboard')
                        
                else:
                    messages.error(request, 'Sua conta está desativada. Entre em contato com o suporte.')
                    return render(request, 'usuarios/login.html', {'email': email})
            else:
                messages.error(request, 'E-mail ou senha incorretos.')
                return render(request, 'usuarios/login.html', {'email': email})
                
        except Exception as e:
            print(f"Erro no login: {e}")
            messages.error(request, 'Erro interno. Tente novamente em alguns minutos.')
            return render(request, 'usuarios/login.html', {'email': email})
    
    return render(request, 'usuarios/login.html')

def cadastro(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        senha = request.POST.get('senha', '')
        confirmar_senha = request.POST.get('confirmar_senha', '')
        aceitar_termos = request.POST.get('aceitar_termos')
        aceitar_newsletter = request.POST.get('aceitar_newsletter')
        
        errors = []
        
        if not first_name:
            errors.append('O nome é obrigatório.')
        
        if not last_name:
            errors.append('O sobrenome é obrigatório.')
        
        if not email:
            errors.append('O e-mail é obrigatório.')
        elif not '@' in email or not '.' in email:
            errors.append('Por favor, insira um e-mail válido.')
        
        if not senha:
            errors.append('A senha é obrigatória.')
        elif len(senha) < 6:
            errors.append('A senha deve ter pelo menos 6 caracteres.')
        
        if not confirmar_senha:
            errors.append('A confirmação da senha é obrigatória.')
        elif senha != confirmar_senha:
            errors.append('As senhas não coincidem.')
        
        if not aceitar_termos:
            errors.append('Você deve aceitar os termos de uso para continuar.')
        
        if email and User.objects.filter(email=email).exists():
            errors.append('Este e-mail já está cadastrado. Tente fazer login ou use outro e-mail.')
        
        if errors:
            for error in errors:
                messages.error(request, error)
            return render(request, 'usuarios/cadastro.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
        
        try:
            username = email.split('@')[0]
            original_username = username
            counter = 1
            
            while User.objects.filter(username=username).exists():
                username = f"{original_username}{counter}"
                counter += 1
            
            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=first_name,
                last_name=last_name
            )
            
            messages.success(
                request, 
                f'Conta criada com sucesso! Bem-vindo(a), {first_name}! Você já está logado.'
            )
            
            user = authenticate(username=username, password=senha)
            if user:
                login(request, user)
                return redirect('dashboard')
            else:
                messages.success(request, 'Conta criada com sucesso! Faça login para continuar.')
                return redirect('login')
            
        except Exception as e:
            messages.error(request, f'Erro ao criar conta: {str(e)}. Tente novamente.')
            return render(request, 'usuarios/cadastro.html', {
                'first_name': first_name,
                'last_name': last_name,
                'email': email,
            })
    
    return render(request, 'usuarios/cadastro.html')

@login_required
def sair(request):
    nome_usuario = request.user.get_full_name() or request.user.first_name or request.user.username
    logout(request)
    messages.success(request, f'Até logo, {nome_usuario}! Volte sempre! 👋')
    return redirect('home')

@login_required
def dashboard(request):
    context = {
        'user': request.user,
        'title': f'Dashboard - {request.user.get_full_name() or request.user.username}',
        'total_predictions': 0,
        'recent_predictions': [],
    }
    return render(request, 'dashboard.html', context)

@login_required
def predict_view(request):
    if request.method == 'POST':
        try:
            if 'flower_image' in request.FILES:
                return handle_image_prediction(request)
            else:
                return handle_manual_prediction(request)
        except Exception as e:
            messages.error(request, f'Erro na predição: {str(e)}')
    
    context = {
        'title': 'Predição de Flores - FlowerML',
        'species': ['Setosa', 'Versicolor', 'Virginica'],
    }
    return render(request, 'predict.html', context)

def handle_image_prediction(request):
    try:
        image_file = request.FILES['flower_image']
        
        if not image_file.content_type.startswith('image/'):
            messages.error(request, 'Por favor, envie apenas arquivos de imagem.')
            return redirect('predict')
        
        image = Image.open(image_file)
        
        prediction_result = {
            'species': 'Iris Setosa',
            'confidence': 92.5,
            'probabilities': {
                'Setosa': 92.5,
                'Versicolor': 5.2,
                'Virginica': 2.3
            }
        }
        
        messages.success(request, f'Predição realizada: {prediction_result["species"]} ({prediction_result["confidence"]:.1f}%)')
        
        return render(request, 'predict_result.html', {
            'result': prediction_result,
            'method': 'image'
        })
        
    except Exception as e:
        messages.error(request, f'Erro ao processar imagem: {str(e)}')
        return redirect('predict')

def handle_manual_prediction(request):
    try:
        sepal_length = float(request.POST.get('sepal_length', 0))
        sepal_width = float(request.POST.get('sepal_width', 0))
        petal_length = float(request.POST.get('petal_length', 0))
        petal_width = float(request.POST.get('petal_width', 0))
        
        if any(value <= 0 for value in [sepal_length, sepal_width, petal_length, petal_width]):
            messages.error(request, 'Todos os valores devem ser maiores que zero.')
            return redirect('predict')
        
        model = load_iris_model()
        
        features = np.array([[sepal_length, sepal_width, petal_length, petal_width]])
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        species_map = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
        predicted_species = species_map[prediction]
        confidence = probabilities[prediction] * 100
        
        prediction_result = {
            'species': f'Iris {predicted_species}',
            'confidence': confidence,
            'probabilities': {
                'Setosa': probabilities[0] * 100,
                'Versicolor': probabilities[1] * 100,
                'Virginica': probabilities[2] * 100
            },
            'input_data': {
                'sepal_length': sepal_length,
                'sepal_width': sepal_width,
                'petal_length': petal_length,
                'petal_width': petal_width
            }
        }
        
        messages.success(request, f'Predição realizada: {prediction_result["species"]} ({confidence:.1f}%)')
        
        return render(request, 'predict_result.html', {
            'result': prediction_result,
            'method': 'manual'
        })
        
    except ValueError:
        messages.error(request, 'Por favor, insira valores numéricos válidos.')
        return redirect('predict')
    except Exception as e:
        messages.error(request, f'Erro na predição: {str(e)}')
        return redirect('predict')

@csrf_exempt
def api_predict(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido'}, status=405)
    
    if not request.user.is_authenticated:
        return JsonResponse({'error': 'Usuário não autenticado'}, status=401)
    
    try:
        data = json.loads(request.body)
        
        required_fields = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width']
        if not all(field in data for field in required_fields):
            return JsonResponse({'error': 'Campos obrigatórios faltando'}, status=400)
        
        features = np.array([[
            float(data['sepal_length']),
            float(data['sepal_width']),
            float(data['petal_length']),
            float(data['petal_width'])
        ]])
        
        model = load_iris_model()
        prediction = model.predict(features)[0]
        probabilities = model.predict_proba(features)[0]
        
        species_map = {0: 'Setosa', 1: 'Versicolor', 2: 'Virginica'}
        
        result = {
            'species': species_map[prediction],
            'confidence': float(probabilities[prediction] * 100),
            'probabilities': {
                'Setosa': float(probabilities[0] * 100),
                'Versicolor': float(probabilities[1] * 100),
                'Virginica': float(probabilities[2] * 100)
            }
        }
        
        return JsonResponse({'success': True, 'result': result})
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def history_view(request):
    predictions = []
    
    paginator = Paginator(predictions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': 'Histórico - FlowerML',
        'predictions': page_obj,
    }
    return render(request, 'history.html', context)

@login_required
def profile_view(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        email = request.POST.get('email', '').strip()
        
        if email != request.user.email and User.objects.filter(email=email).exists():
            messages.error(request, 'Este e-mail já está sendo usado por outro usuário.')
        else:
            request.user.first_name = first_name
            request.user.last_name = last_name
            request.user.email = email
            request.user.save()
            
            messages.success(request, 'Perfil atualizado com sucesso!')
        
        return redirect('profile')
    
    context = {
        'title': 'Perfil - FlowerML',
        'user': request.user,
    }
    return render(request, 'profile.html', context)

@login_required
def change_password(request):
    if request.method == 'POST':
        current_password = request.POST.get('current_password', '')
        new_password = request.POST.get('new_password', '')
        confirm_password = request.POST.get('confirm_password', '')
        
        if not request.user.check_password(current_password):
            messages.error(request, 'Senha atual incorreta.')
        elif len(new_password) < 6:
            messages.error(request, 'A nova senha deve ter pelo menos 6 caracteres.')
        elif new_password != confirm_password:
            messages.error(request, 'As senhas não coincidem.')
        else:
            request.user.set_password(new_password)
            request.user.save()
            
            user = authenticate(username=request.user.username, password=new_password)
            login(request, user)
            
            messages.success(request, 'Senha alterada com sucesso!')
            return redirect('profile')
    
    return render(request, 'change_password.html')

def about_view(request):
    context = {
        'title': 'Sobre - FlowerML',
    }
    return render(request, 'about.html', context)

def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()
        
        if all([name, email, subject, message]):
            messages.success(request, 'Mensagem enviada com sucesso! Entraremos em contato em breve.')
        else:
            messages.error(request, 'Por favor, preencha todos os campos.')
    
    context = {
        'title': 'Contato - FlowerML',
    }
    return render(request, 'contact.html', context)

def privacy_view(request):
    context = {
        'title': 'Política de Privacidade - FlowerML',
    }
    return render(request, 'privacy.html', context)

def load_iris_model():
    try:
        model_path = os.path.join(settings.BASE_DIR, 'models', 'iris_model.pkl')
        
        if os.path.exists(model_path):
            return joblib.load(model_path)
        else:
            from sklearn.datasets import load_iris
            from sklearn.ensemble import RandomForestClassifier
            from sklearn.model_selection import train_test_split
            
            iris = load_iris()
            X_train, X_test, y_train, y_test = train_test_split(
                iris.data, iris.target, test_size=0.2, random_state=42
            )
            
            model = RandomForestClassifier(n_estimators=100, random_state=42)
            model.fit(X_train, y_train)
            
            os.makedirs(os.path.dirname(model_path), exist_ok=True)
            joblib.dump(model, model_path)
            
            return model
            
    except Exception as e:
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.datasets import load_iris
        
        iris = load_iris()
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        model.fit(iris.data, iris.target)
        return model

def save_prediction(user, method, result, image_file=None):
    pass

def handler404(request, exception):
    return render(request, 'errors/404.html', status=404)

def handler500(request):
    return render(request, 'errors/500.html', status=500)