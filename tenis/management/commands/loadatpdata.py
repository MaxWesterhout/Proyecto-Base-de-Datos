from django.core.management.base import BaseCommand, CommandError
from tenis.models import Country, Player, Match, Tournament, Ranking, PlayerMatchStats

import csv, datetime, codecs

class Command(BaseCommand):
    def handle(self, *args, **kwargs):
		#load countries
        obsolete = {
            "MSH":"MHL",
            "MGO":"MNE",
            "SIN":"SGP"
        }

        self.stdout.write("Loading countries")
        with open("tenis/data/country-codes.csv") as f:
            reader = csv.DictReader(f)
            for x in Country.objects.iterator(): x.delete()
            for row in reader:
                if not row["IOC"] == "" and not bytes(row["IOC"], "utf-8").replace(b"\xc2\xa0", b" ") == b" ":
                    #self.stdout.write("Found country "+row["IOC"]+" "+row["CLDR display name"])
                    ioc = obsolete[row["IOC"]] if row["IOC"] in obsolete else row["IOC"]
                    _, created = Country.objects.get_or_create(
                        ioc = ioc,
                        name = row["UNTERM English Short"]
                    )

        #load historical countries
        with open("tenis/data/historical_noc.csv") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if not row["IOC"] == "" and not bytes(row["IOC"], "utf-8").replace(b"\xc2\xa0", b" ") == b" ":
                    #self.stdout.write("Found country "+row["IOC"]+" "+row["CLDR display name"])
                    _, created = Country.objects.get_or_create(
                        ioc = row["IOC"],
                        name = row["CLDR display name"]
                    )

        #load players
        obsolete = {
            "TRI":"TTO",
            "UNK":None,
            "ECA":None,
            "CAR":"CAF",
            "RHO":"ZIM",
            "BRI":"GBR",
            "HAW":"USA",
            "NMI":"USA",
            "CAL":"FRA",
            "POC":None,
            "SIN":"SGP",
            "ITF":"ITA",
            "CUW":None,
            "":None,
            "LVA":"LAT",
            "TGO":"TOG",
            "HRV":"CRO",
            "CHE":"SUI",
            "MYS":"MAS",
            "DNK":"DEN",
            "DEU":"GER"
        }

        with open("tenis/data/atp_players.csv") as f:
            reader = csv.reader(f)
            self.stdout.write("Deleting players")
            for x in Player.objects.iterator(): x.delete()
            self.stdout.write("Loading players")
            for row in reader:
                id, name, last_name, handedness, dob, ioc = row
                ioc = obsolete[ioc] if ioc in obsolete else ioc
                ioc = Country.objects.get(ioc=ioc) if ioc!=None else None
                if (bytes(dob, "utf-8").replace(b"\xc2\xa0", b" ") == b" " or dob==""):
                    dob = None
                else:
                    year = int(dob[0:4])
                    month = dob[4:6]
                    month = 1 if month=="" else max(1,int(month))
                    day = dob[6:8]
                    day = 1 if day=="" else max(1,int(day))
                    dob = datetime.date(year,month,day)
                self.stdout.write("Found player: "+ str([id, name, last_name, handedness, dob, ioc]))
                _, created = Player.objects.get_or_create(
                    id = id,
                    name = name,
                    last_name = last_name,
                    handedness = handedness,
                    dob = dob,
                    ioc = ioc,
                )

        #load rankings
        for x in Ranking.objects.iterator(): x.delete()
        self.stdout.write("Loading rankings")
        with open("tenis/data/atp_rankings_current.csv") as f:
            reader = csv.DictReader(f)
            k = 0
            bulk = []
            for row in reader:
                date_string = row["ranking_date"]
                points = row["points"]
                points = 0 if points=="" else int(points)
                obj = Ranking(
                    player = Player.objects.get(id=row["player"]),
                    date = datetime.date(int(date_string[0:4]), int(date_string[4:6]), int(date_string[6:8])),
                    rank = row["rank"],
                    points = points
                )
                bulk.extend([obj])
                k+=1
                if k%1000 == 0:
                    self.stdout.write(str(k))
                    Ranking.objects.bulk_create(bulk)
                    bulk.clear()
            Ranking.objects.bulk_create(bulk)
            
        self.stdout.write("Finding ranking duplicates")
        for x in Ranking.objects.iterator():
            duplicates = Ranking.objects.filter(date=x.date,player=x.player).order_by("-points")
            if len(duplicates)>1:
                self.stdout.write("Found duplicate for: "+str(x.date)+" "+str(x.player))
                for i in range(1,len(duplicates)):
                    duplicates[i].delete()

        #load tournaments, matches, and stats
        for x in Tournament.objects.iterator(): x.delete()
        for x in Match.objects.iterator(): x.delete()
        for x in PlayerMatchStats.objects.iterator(): x.delete()
        self.stdout.write("Loading tournaments")
        for year in range(2000,2022):
            with open("tenis/data/atp_matches_"+str(year)+".csv") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    tourney_id = row["tourney_id"]
                    tourney_name = row["tourney_name"]
                    t_start_date = row["tourney_date"]
                    t_start_date = datetime.date(int(t_start_date[0:4]),int(t_start_date[4:6]),int(t_start_date[6:8]))
                    t_level = row["tourney_level"]
                    t_surface = row["surface"]
                    tournament_obj, created = Tournament.objects.get_or_create(
                        id = tourney_id,
                        name = tourney_name,
                        start_date = t_start_date,
                        level = t_level,
                        surface = t_surface
                    )
                    if not created and tournament_obj.name != row["tourney_name"] and tournament_obj.id == row["tourney_id"]:
                        self.stderr.write("Integrity: " + tournament_obj.name + " and " + row["tourney_name"] + " both have ID " + tournament_obj.id)				

                    match_obj, created = Match.objects.get_or_create(
                        tournament = tournament_obj,
                        match_num = row["match_num"],
                        best_of = row["best_of"],
                        round = row["round"],
                        score = row["score"]
                    )

                    height = row["winner_ht"]
                    height = None if height=='' else height
                    _, created = PlayerMatchStats.objects.get_or_create(
                        match = match_obj,
                        player = Player.objects.get(id=row["winner_id"]),
                        result = PlayerMatchStats.Result.WINNER,
                        height = height,
                    )

                    height = row["loser_ht"]
                    height = None if height=='' else height
                    _, created = PlayerMatchStats.objects.get_or_create(
                        match = match_obj,
                        player = Player.objects.get(id=row["loser_id"]),
                        result = PlayerMatchStats.Result.LOSER,
                        height = height,
                    )
                    self.stdout.write("Tournament: "+str(tourney_id)+" "+str(row["match_num"]))