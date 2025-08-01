from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash
import json
import os
from datetime import datetime
import requests
import urllib.parse

app = Flask(__name__)
app.secret_key = 'agrotechhub_secret_key_2024'

# Simulação de banco de dados em memória
users_db = {
    'admin@agro.com': {
        'password': '123456',
        'name': 'João Silva',
        'type': 'produtor'
    }
}

plantations_db = []
products_db = [
    {
        'id': 1,
        'name': 'Sementes de Soja Premium',
        'category': 'sementes',
        'price': 'R$ 180,00/saca',
        'description': 'Sementes de soja de alta qualidade, resistente a pragas',
        'image': '/static/images/soja-seeds.jpg',
        'contact': '(11) 99999-1111'
    },
    {
        'id': 2,
        'name': 'Fertilizante NPK 20-05-20',
        'category': 'insumos',
        'price': 'R$ 95,00/saca',
        'description': 'Fertilizante completo para todas as culturas',
        'image': '/static/images/fertilizer.jpg',
        'contact': '(11) 99999-2222'
    },
    {
        'id': 3,
        'name': 'Trator Compacto 75CV',
        'category': 'equipamentos',
        'price': 'R$ 85.000,00',
        'description': 'Trator compacto ideal para pequenas propriedades',
        'image': '/static/images/tractor.jpg',
        'contact': '(11) 99999-3333'
    }
]

blog_posts = [
    {
        'id': 1,
        'title': 'Agricultura de Precisão: O Futuro da Produção',
        'content': 'A agricultura de precisão utiliza tecnologias avançadas como GPS, sensores e drones para otimizar a produção agrícola...',
        'date': '2024-01-15',
        'author': 'Dr. Maria Santos'
    },
    {
        'id': 2,
        'title': 'Sustentabilidade no Campo: Práticas Essenciais',
        'content': 'Implementar práticas sustentáveis na agricultura não é apenas uma responsabilidade ambiental, mas também uma estratégia econômica...',
        'date': '2024-01-10',
        'author': 'Eng. Carlos Oliveira'
    }
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email in users_db and users_db[email]['password'] == password:
            session['user'] = email
            session['user_name'] = users_db[email]['name']
            session['user_type'] = users_db[email]['type']
            flash('Login realizado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha incorretos!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user_type = request.form['user_type']
        
        if email not in users_db:
            users_db[email] = {
                'password': password,
                'name': name,
                'type': user_type
            }
            flash('Cadastro realizado com sucesso!', 'success')
            return redirect(url_for('login'))
        else:
            flash('Email já cadastrado!', 'error')
    
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    user_plantations = [p for p in plantations_db if p['owner'] == session['user']]
    return render_template('dashboard.html', plantations=user_plantations)

@app.route('/add_plantation', methods=['GET', 'POST'])
def add_plantation():
    if 'user' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        plantation = {
            'id': len(plantations_db) + 1,
            'name': request.form['name'],
            'culture_type': request.form['culture_type'],
            'location': request.form['location'],
            'harvest_date': request.form['harvest_date'],
            'image': request.form['image'],
            'owner': session['user'],
            'created_at': datetime.now().strftime('%Y-%m-%d')
        }
        plantations_db.append(plantation)
        flash('Plantação cadastrada com sucesso!', 'success')
        return redirect(url_for('dashboard'))
    
    return render_template('add_plantation.html')

@app.route('/products')
def products():
    return render_template('products.html', products=products_db)

@app.route('/weather')
def weather():
    return render_template('weather.html')

@app.route('/api/weather/<city>')
def get_weather(city):
    try:
        # Usar múltiplas APIs para garantir dados reais
        weather_data = None
        
        # Primeira tentativa: wttr.in (mais confiável)
        try:
            weather_data = get_weather_from_wttr(city)
        except:
            pass
        
        # Segunda tentativa: OpenMeteo (backup)
        if not weather_data:
            try:
                weather_data = get_weather_from_openmeteo(city)
            except:
                pass
        
        # Terceira tentativa: WeatherAPI (backup 2)
        if not weather_data:
            try:
                weather_data = get_weather_from_weatherapi(city)
            except:
                pass
        
        if not weather_data:
            return jsonify({'error': 'Não foi possível obter dados meteorológicos para esta cidade'}), 404
            
        return jsonify(weather_data)
        
    except Exception as e:
        print(f"Erro geral: {e}")
        return jsonify({'error': 'Erro interno do servidor'}), 500

def get_weather_from_wttr(city):
    """Obter dados do wttr.in"""
    url = f"https://wttr.in/{urllib.parse.quote(city)}?format=j1"
    
    response = requests.get(url, timeout=10, headers={
        'User-Agent': 'AgroTechHub/1.0'
    })
    
    if response.status_code != 200:
        raise Exception("Falha na API wttr.in")
        
    data = response.json()
    
    # Verificar se os dados são válidos
    if 'current_condition' not in data or not data['current_condition']:
        raise Exception("Dados inválidos do wttr.in")
    
    current = data['current_condition'][0]
    
    # Traduzir condições climáticas
    weather_translations = {
        'Sunny': 'Ensolarado', 'Clear': 'Limpo', 'Partly cloudy': 'Parcialmente nublado',
        'Cloudy': 'Nublado', 'Overcast': 'Encoberto', 'Mist': 'Névoa',
        'Patchy rain possible': 'Possibilidade de chuva', 'Patchy snow possible': 'Possibilidade de neve',
        'Patchy sleet possible': 'Possibilidade de granizo', 'Thundery outbreaks possible': 'Possibilidade de trovoadas',
        'Blowing snow': 'Neve com vento', 'Blizzard': 'Nevasca', 'Fog': 'Neblina',
        'Freezing fog': 'Neblina congelante', 'Patchy light drizzle': 'Garoa leve irregular',
        'Light drizzle': 'Garoa leve', 'Freezing drizzle': 'Garoa congelante',
        'Heavy freezing drizzle': 'Garoa congelante forte', 'Patchy light rain': 'Chuva leve irregular',
        'Light rain': 'Chuva leve', 'Moderate rain at times': 'Chuva moderada ocasional',
        'Moderate rain': 'Chuva moderada', 'Heavy rain at times': 'Chuva forte ocasional',
        'Heavy rain': 'Chuva forte', 'Light freezing rain': 'Chuva congelante leve',
        'Moderate or heavy freezing rain': 'Chuva congelante moderada a forte',
        'Light sleet': 'Granizo leve', 'Moderate or heavy sleet': 'Granizo moderado a forte',
        'Patchy light snow': 'Neve leve irregular', 'Light snow': 'Neve leve',
        'Patchy moderate snow': 'Neve moderada irregular', 'Moderate snow': 'Neve moderada',
        'Patchy heavy snow': 'Neve forte irregular', 'Heavy snow': 'Neve forte',
        'Ice pellets': 'Granizo', 'Light rain shower': 'Pancada de chuva leve',
        'Moderate or heavy rain shower': 'Pancada de chuva moderada a forte',
        'Torrential rain shower': 'Pancada de chuva torrencial',
        'Light sleet showers': 'Pancadas de granizo leve',
        'Moderate or heavy sleet showers': 'Pancadas de granizo moderado a forte',
        'Light snow showers': 'Pancadas de neve leve',
        'Moderate or heavy snow showers': 'Pancadas de neve moderada a forte',
        'Light showers of ice pellets': 'Pancadas leves de granizo',
        'Moderate or heavy showers of ice pellets': 'Pancadas moderadas a fortes de granizo',
        'Patchy light rain with thunder': 'Chuva leve irregular com trovoadas',
        'Moderate or heavy rain with thunder': 'Chuva moderada a forte com trovoadas',
        'Patchy light snow with thunder': 'Neve leve irregular com trovoadas',
        'Moderate or heavy snow with thunder': 'Neve moderada a forte com trovoadas'
    }
    
    description = current['weatherDesc'][0]['value']
    translated_desc = weather_translations.get(description, description)
    
    # Obter informações de localização mais precisas
    nearest_area = data.get('nearest_area', [{}])[0]
    city_name = nearest_area.get('areaName', [{'value': city}])[0]['value']
    country = nearest_area.get('country', [{'value': ''}])[0]['value']
    region = nearest_area.get('region', [{'value': ''}])[0]['value']
    
    # Formatar nome da localização
    location_parts = [city_name]
    if region and region != city_name:
        location_parts.append(region)
    if country:
        location_parts.append(country)
    
    weather_data = {
        'city': ', '.join(location_parts),
        'temperature': int(current['temp_C']),
        'feels_like': int(current['FeelsLikeC']),
        'humidity': int(current['humidity']),
        'description': translated_desc,
        'wind_speed': int(float(current['windspeedKmph'])),
        'pressure': int(current['pressure']),
        'visibility': int(current['visibility']),
        'icon': get_weather_icon(current['weatherCode']),
        'uv_index': int(current.get('uvIndex', 0)),
        'forecast': []
    }
    
    # Processar previsão dos próximos dias
    for i, day_data in enumerate(data['weather'][:5]):
        day_name = get_day_name(i)
        
        min_temp = int(day_data['mintempC'])
        max_temp = int(day_data['maxtempC'])
        condition = day_data['hourly'][4]['weatherDesc'][0]['value']  # Meio-dia
        translated_condition = weather_translations.get(condition, condition)
        icon_code = day_data['hourly'][4]['weatherCode']
        
        weather_data['forecast'].append({
            'day': day_name,
            'temp_max': max_temp,
            'temp_min': min_temp,
            'condition': translated_condition,
            'icon': get_weather_icon(icon_code)
        })
    
    return weather_data

def get_weather_from_openmeteo(city):
    """Backup: OpenMeteo API (gratuita)"""
    # Primeiro, obter coordenadas da cidade
    geocoding_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1&language=pt&format=json"
    
    geo_response = requests.get(geocoding_url, timeout=10)
    if geo_response.status_code != 200:
        raise Exception("Falha na geocodificação")
    
    geo_data = geo_response.json()
    if not geo_data.get('results'):
        raise Exception("Cidade não encontrada")
    
    location = geo_data['results'][0]
    lat, lon = location['latitude'], location['longitude']
    
    # Obter dados meteorológicos
    weather_url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,surface_pressure,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min&timezone=auto&forecast_days=5"
    
    weather_response = requests.get(weather_url, timeout=10)
    if weather_response.status_code != 200:
        raise Exception("Falha na API meteorológica")
    
    weather_data_raw = weather_response.json()
    current = weather_data_raw['current']
    daily = weather_data_raw['daily']
    
    # Mapear códigos de clima do OpenMeteo
    weather_code_map = {
        0: 'Limpo', 1: 'Principalmente limpo', 2: 'Parcialmente nublado', 3: 'Nublado',
        45: 'Neblina', 48: 'Neblina com geada', 51: 'Garoa leve', 53: 'Garoa moderada',
        55: 'Garoa intensa', 56: 'Garoa congelante leve', 57: 'Garoa congelante intensa',
        61: 'Chuva leve', 63: 'Chuva moderada', 65: 'Chuva intensa',
        66: 'Chuva congelante leve', 67: 'Chuva congelante intensa',
        71: 'Neve leve', 73: 'Neve moderada', 75: 'Neve intensa',
        77: 'Grãos de neve', 80: 'Pancadas de chuva leves', 81: 'Pancadas de chuva moderadas',
        82: 'Pancadas de chuva violentas', 85: 'Pancadas de neve leves', 86: 'Pancadas de neve intensas',
        95: 'Trovoada', 96: 'Trovoada com granizo leve', 99: 'Trovoada com granizo intenso'
    }
    
    city_display = f"{location['name']}, {location['country']}"
    
    weather_data = {
        'city': city_display,
        'temperature': int(current['temperature_2m']),
        'feels_like': int(current['apparent_temperature']),
        'humidity': int(current['relative_humidity_2m']),
        'description': weather_code_map.get(current['weather_code'], 'Desconhecido'),
        'wind_speed': int(current['wind_speed_10m']),
        'pressure': int(current['surface_pressure']),
        'visibility': 10,  # OpenMeteo não fornece visibilidade
        'icon': get_weather_icon_openmeteo(current['weather_code']),
        'uv_index': 0,  # OpenMeteo não fornece UV na versão gratuita
        'forecast': []
    }
    
    # Processar previsão
    for i in range(5):
        day_name = get_day_name(i)
        weather_data['forecast'].append({
            'day': day_name,
            'temp_max': int(daily['temperature_2m_max'][i]),
            'temp_min': int(daily['temperature_2m_min'][i]),
            'condition': weather_code_map.get(daily['weather_code'][i], 'Desconhecido'),
            'icon': get_weather_icon_openmeteo(daily['weather_code'][i])
        })
    
    return weather_data

def get_weather_from_weatherapi(city):
    """Backup 2: WeatherAPI (versão gratuita limitada)"""
    # Esta é uma API que oferece algumas consultas gratuitas
    url = f"http://api.weatherapi.com/v1/forecast.json?key=demo&q={urllib.parse.quote(city)}&days=5&aqi=no&alerts=no"
    
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        raise Exception("Falha na WeatherAPI")
    
    data = response.json()
    current = data['current']
    location = data['location']
    forecast = data['forecast']['forecastday']
    
    weather_data = {
        'city': f"{location['name']}, {location['country']}",
        'temperature': int(current['temp_c']),
        'feels_like': int(current['feelslike_c']),
        'humidity': int(current['humidity']),
        'description': current['condition']['text'],
        'wind_speed': int(current['wind_kph']),
        'pressure': int(current['pressure_mb']),
        'visibility': int(current['vis_km']),
        'icon': get_weather_icon_from_condition(current['condition']['text']),
        'uv_index': int(current.get('uv', 0)),
        'forecast': []
    }
    
    # Processar previsão
    for i, day in enumerate(forecast[:5]):
        day_name = get_day_name(i)
        day_data = day['day']
        weather_data['forecast'].append({
            'day': day_name,
            'temp_max': int(day_data['maxtemp_c']),
            'temp_min': int(day_data['mintemp_c']),
            'condition': day_data['condition']['text'],
            'icon': get_weather_icon_from_condition(day_data['condition']['text'])
        })
    
    return weather_data

def get_weather_icon(weather_code):
    """Converte código do clima em ícone Font Awesome"""
    code = str(weather_code)
    
    icon_map = {
        '113': 'fas fa-sun', '116': 'fas fa-cloud-sun', '119': 'fas fa-cloud',
        '122': 'fas fa-cloud', '143': 'fas fa-smog', '176': 'fas fa-cloud-rain',
        '179': 'fas fa-cloud-snow', '182': 'fas fa-cloud-rain', '185': 'fas fa-cloud-rain',
        '200': 'fas fa-bolt', '227': 'fas fa-wind', '230': 'fas fa-snowflake',
        '248': 'fas fa-smog', '260': 'fas fa-smog', '263': 'fas fa-cloud-rain',
        '266': 'fas fa-cloud-rain', '281': 'fas fa-cloud-rain', '284': 'fas fa-cloud-rain',
        '293': 'fas fa-cloud-rain', '296': 'fas fa-cloud-rain', '299': 'fas fa-cloud-rain',
        '302': 'fas fa-cloud-rain', '305': 'fas fa-cloud-showers-heavy', '308': 'fas fa-cloud-showers-heavy',
        '311': 'fas fa-cloud-rain', '314': 'fas fa-cloud-rain', '317': 'fas fa-icicles',
        '320': 'fas fa-icicles', '323': 'fas fa-cloud-snow', '326': 'fas fa-cloud-snow',
        '329': 'fas fa-cloud-snow', '332': 'fas fa-cloud-snow', '335': 'fas fa-cloud-snow',
        '338': 'fas fa-cloud-snow', '350': 'fas fa-icicles', '353': 'fas fa-cloud-rain',
        '356': 'fas fa-cloud-showers-heavy', '359': 'fas fa-cloud-showers-heavy',
        '362': 'fas fa-icicles', '365': 'fas fa-icicles', '368': 'fas fa-cloud-snow',
        '371': 'fas fa-cloud-snow', '374': 'fas fa-icicles', '377': 'fas fa-icicles',
        '386': 'fas fa-bolt', '389': 'fas fa-bolt', '392': 'fas fa-bolt', '395': 'fas fa-bolt'
    }
    
    return icon_map.get(code, 'fas fa-sun')

def get_weather_icon_openmeteo(weather_code):
    """Ícones para códigos do OpenMeteo"""
    icon_map = {
        0: 'fas fa-sun', 1: 'fas fa-cloud-sun', 2: 'fas fa-cloud-sun', 3: 'fas fa-cloud',
        45: 'fas fa-smog', 48: 'fas fa-smog', 51: 'fas fa-cloud-rain', 53: 'fas fa-cloud-rain',
        55: 'fas fa-cloud-rain', 56: 'fas fa-cloud-rain', 57: 'fas fa-cloud-rain',
        61: 'fas fa-cloud-rain', 63: 'fas fa-cloud-rain', 65: 'fas fa-cloud-showers-heavy',
        66: 'fas fa-cloud-rain', 67: 'fas fa-cloud-rain', 71: 'fas fa-cloud-snow',
        73: 'fas fa-cloud-snow', 75: 'fas fa-cloud-snow', 77: 'fas fa-cloud-snow',
        80: 'fas fa-cloud-rain', 81: 'fas fa-cloud-rain', 82: 'fas fa-cloud-showers-heavy',
        85: 'fas fa-cloud-snow', 86: 'fas fa-cloud-snow', 95: 'fas fa-bolt',
        96: 'fas fa-bolt', 99: 'fas fa-bolt'
    }
    return icon_map.get(weather_code, 'fas fa-sun')

def get_weather_icon_from_condition(condition):
    """Ícones baseados na descrição textual"""
    condition_lower = condition.lower()
    
    if 'sun' in condition_lower or 'clear' in condition_lower:
        return 'fas fa-sun'
    elif 'cloud' in condition_lower and ('part' in condition_lower or 'few' in condition_lower):
        return 'fas fa-cloud-sun'
    elif 'cloud' in condition_lower:
        return 'fas fa-cloud'
    elif 'rain' in condition_lower or 'shower' in condition_lower:
        return 'fas fa-cloud-rain'
    elif 'snow' in condition_lower:
        return 'fas fa-cloud-snow'
    elif 'thunder' in condition_lower or 'storm' in condition_lower:
        return 'fas fa-bolt'
    elif 'fog' in condition_lower or 'mist' in condition_lower:
        return 'fas fa-smog'
    else:
        return 'fas fa-sun'

def get_day_name(index):
    """Retorna o nome do dia baseado no índice"""
    if index == 0:
        return 'Hoje'
    elif index == 1:
        return 'Amanhã'
    else:
        days = ['Segunda', 'Terça', 'Quarta', 'Quinta', 'Sexta', 'Sábado', 'Domingo']
        from datetime import datetime, timedelta
        future_date = datetime.now() + timedelta(days=index)
        day_index = future_date.weekday()
        return days[day_index]

@app.route('/blog')
def blog():
    return render_template('blog.html', posts=blog_posts)

@app.route('/logout')
def logout():
    session.clear()
    flash('Logout realizado com sucesso!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
