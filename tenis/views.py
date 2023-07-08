from django.shortcuts import render
from django.http import HttpResponse
from tenis.models import Mes
from django.db import connection
from collections import namedtuple
from django.shortcuts import render
from .forms import NombreMesForm, CountryNameForm, PlayerNameForm, SearchForm

# Create your views here.     
def index(request):
    if request.method == 'GET':
        return render(request, 'tenishome.html')
    else:
        return render(request, 'tenishome.html')

def mayo(request):
    return HttpResponse("El número del mes 'Mayo' es "+str(Mes.objects.filter(nombre='Mayo')[:1].get().numero))

def mayosql(request):
    return HttpResponse("El número del mes 'Mayo' es "+ str(consultar_mes('Mayo')[0].numero))
    
def mes(request):
    # si es POST, tenemos una petición del usuario
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NombreMesForm(request.POST)
        # verifica que sea valido:
        if form.is_valid():
            nombre_mes = form.cleaned_data['nombre_mes']
            sql_res = consultar_mes(nombre_mes)
            if sql_res:
                num_mes = consultar_mes(nombre_mes)[0].numero
                res = 'El número del mes '+nombre_mes+' es '+str(num_mes)
            else:
                res = 'El mes '+nombre_mes+' no está en la tabla'
            return render(request, 'mes_form.html', {'mes_form': form, 'resultados': res})
    # si es GET (o algo diferente) crearemos un formulario en blanco
    else:
        form = NombreMesForm()
    return render(request, 'mes_form.html', {'mes_form': form})

def consultar_mes(mes):
    with connection.cursor() as cursor:
        cursor.execute("SELECT numero FROM tenis.mes WHERE nombre = %s", [mes])
        results = namedtuplefetchall(cursor)
    return results

def country_best(request):
    # si es POST, tenemos una petición del usuario
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = CountryNameForm(request.POST)
        # verifica que sea valido:
        if form.is_valid():
            country_name = form.cleaned_data['country_name']
            ioc_res = get_ioc_from_name(country_name)
            likely_res = get_likely_country(country_name)
            res = ""
            if ioc_res:
                ioc = ioc_res[0].ioc
                country_name = ioc_res[0].name
                best_res = get_country_best_player(ioc)
                if best_res:
                    player_name = best_res[0].name + " " + best_res[0].last_name
                    rank = best_res[0].rank
                    date = best_res[0].date
                    res = 'The best player from ' + country_name + ' is ' + str(player_name) + ", sitting at #" + str(rank) + " as of " + str(date)
                else:
                    res = "No players could be found for " + country_name
            elif likely_res:
                likely_country = likely_res[0].name
                res = "The country "+ country_name + " could not be found. Maybe you meant \""+ likely_country + "\".\n"
                ioc = likely_res[0].ioc
                best_res = get_country_best_player(ioc)
                country_name = likely_country
                if best_res:
                    player_name = best_res[0].name + " " + best_res[0].last_name
                    rank = best_res[0].rank
                    date = best_res[0].date
                    res += 'The best player from ' + country_name + ' is ' + str(player_name) + ", sitting at #" + str(rank) + " as of " + str(date)
                else:
                    res += "No players could be found for " + country_name
            else:
                res = 'The country '+ country_name +' could not be found.'
            return render(request, 'country_best.html', {'country_name_form': form, 'results': res})
    # si es GET (o algo diferente) crearemos un formulario en blanco
    else:
        form = CountryNameForm()
    return render(request, 'country_best.html', {'country_name_form': form})

def latest_result(request):
    # si es POST, tenemos una petición del usuario
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerNameForm(request.POST)
        # verifica que sea valido:
        if form.is_valid():
            player_name = form.cleaned_data['player_name']
            player_last_name = form.cleaned_data['player_last_name']
            id_res = get_player_id(player_name, player_last_name)
            if id_res:
                player_id = id_res[0].id
                latest_res = get_player_latest_result(player_id)
                if latest_res:
                    m_result = latest_res[0].result
                    if m_result=="W": m_result="WIN"
                    if m_result=="L": m_result="LOSS"
                    res = player_name + " " + player_last_name + '\'s last match ended in a ' + m_result + "."
            else:
                res = 'The player '+ player_name + " " + player_last_name +' could not be found.'
            return render(request, 'latest_result.html', {'player_name_form': form, 'results': res})
    # si es GET (o algo diferente) crearemos un formulario en blanco
    else:
        form = PlayerNameForm()
    return render(request, 'latest_result.html', {'player_name_form': form})

def player_tournaments(request):
    # si es POST, tenemos una petición del usuario
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = PlayerNameForm(request.POST)
        # verifica que sea valido:
        if form.is_valid():
            player_name = form.cleaned_data['player_name']
            player_last_name = form.cleaned_data['player_last_name']
            id_res = get_player_id(player_name, player_last_name)
            tournaments = []
            if id_res:
                player_id = id_res[0].id
                player_name = id_res[0].name
                player_last_name = id_res[0].last_name
                tournaments_res = get_player_tournaments(player_id)
                if tournaments_res:
                    for tournament in tournaments_res:
                        t_id = tournament.id
                        t_name = tournament.name
                        t_date = tournament.start_date
                        tournaments.append(str(t_id) + " - " + str(t_name) +  " " + str(t_date))
                    res = player_name + " " + player_last_name + " has played in the following tournaments: "
            else:
                res = 'The player '+ player_name + " " + player_last_name +' could not be found.'
            return render(request, 'player_tournaments.html', {'player_name_form': form, 'results': res, 'tournaments': tournaments})
    # si es GET (o algo diferente) crearemos un formulario en blanco
    else:
        form = PlayerNameForm()
    return render(request, 'player_tournaments.html', {'player_name_form': form})

def search_players(request):
    # si es POST, tenemos una petición del usuario
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SearchForm(request.POST)
        # verifica que sea valido:
        if form.is_valid():
            search_str = form.cleaned_data['search_str']
            search_res = get_players_search(search_str)
            players = []
            if search_res:
                res = "The following players were found for search \'" + search_str + "\':"
                for player in search_res:
                    p_name = player.name + " " + player.last_name
                    if player.ioc_id:
                        p_country = "(" + player.ioc_id + ")"
                    else:
                        p_country = "(" + "UNK" + ")"
                    players.append(str(p_name) + " " + str(p_country))
            else:
                res = 'No players could be found.'
            return render(request, 'search_players.html', {'search_form': form, 'results': res, 'players': players})
    # si es GET (o algo diferente) crearemos un formulario en blanco
    else:
        form = SearchForm()
    return render(request, 'search_players.html', {'search_form': form})

def get_likely_country(country_name):
    with connection.cursor() as cursor:
        country_name = "%" + country_name + "%"
        cursor.execute("""
            SELECT name, ioc
            FROM tenis_country
            WHERE UPPER(name) LIKE UPPER(%s)
        """, [country_name])
        results = namedtuplefetchall(cursor)
    return results

def get_players_search(search_str):
    with connection.cursor() as cursor:
        search_str = "%" + search_str + "%"
        cursor.execute("""
            SELECT *
            FROM tenis_player
            WHERE UPPER(name) LIKE UPPER(%s) OR UPPER(last_name) LIKE UPPER(%s)
        """, [search_str, search_str])
        results = namedtuplefetchall(cursor)
    return results

def get_player_id(name, last_name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT id, name, last_name
            FROM tenis_player
            WHERE UPPER(name)=UPPER(%s) AND UPPER(last_name)=UPPER(%s)
        """, [name, last_name])
        results = namedtuplefetchall(cursor)
    return results

def get_ioc_from_name(name):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT ioc, name
            FROM tenis_country
            WHERE UPPER(name)=UPPER(%s)
        """, [name])
        results = namedtuplefetchall(cursor)
    return results

def get_country_best_player(ioc):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT P.name, P.last_name, R.rank, R.date
            FROM tenis_ranking R JOIN tenis_player P
            ON P.id = R.player_id
            WHERE P.ioc_id = %s
            AND R.date >= ALL (
                SELECT R2.date
                FROM tenis_ranking R2 JOIN tenis_player P2
                ON P2.id = R2.player_id
                WHERE P2.id = P.id
                )
            ORDER BY R.rank ASC
            LIMIT 1
        """, [ioc])
        results = namedtuplefetchall(cursor)
    return results

def get_player_tournaments(player_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT DISTINCT tenis_tournament.id, tenis_tournament.name, tenis_tournament.start_date
            FROM tenis_match JOIN tenis_playermatchstats
            ON tenis_match.id = tenis_playermatchstats.match_id
            JOIN tenis_tournament
            ON tenis_match.tournament_id = tenis_tournament.id
            WHERE tenis_playermatchstats.player_id = %s
            ORDER BY tenis_tournament.start_date DESC
        """, [player_id])
        results = namedtuplefetchall(cursor)
    return results

def get_player_latest_result(player_id):
    tournament_id = get_player_latest_tournament(player_id)[0].tournament_id
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tenis_playermatchstats.result
            FROM tenis_match JOIN tenis_playermatchstats
            ON tenis_match.id = tenis_playermatchstats.match_id
            JOIN tenis_tournament
            ON tenis_match.tournament_id = tenis_tournament.id
            WHERE tenis_playermatchstats.player_id = %s
            AND tenis_match.tournament_id = %s
            ORDER BY tenis_match.match_num DESC
            LIMIT 1
        """, [player_id, tournament_id])
        results = namedtuplefetchall(cursor)
    return results

def get_player_latest_tournament(player_id):
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT tenis_match.tournament_id
            FROM tenis_match JOIN tenis_playermatchstats
            ON tenis_match.id = tenis_playermatchstats.match_id
            JOIN tenis_tournament
            ON tenis_match.tournament_id = tenis_tournament.id
            WHERE tenis_playermatchstats.player_id = %s
            ORDER BY tenis_tournament.start_date DESC
            LIMIT 1
        """, [player_id])
        results = namedtuplefetchall(cursor)
    return results

def namedtuplefetchall(cursor):
    "Return all rows from a cursor as a namedtuple"
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]
   