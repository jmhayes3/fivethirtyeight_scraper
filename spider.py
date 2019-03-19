import scrapy
from scrapy.crawler import CrawlerProcess

class GamesSpider(scrapy.Spider):
    name = 'games'

    def start_requests(self):
        yield scrapy.Request('https://projects.fivethirtyeight.com/2019-nba-predictions/games/', self.parse)

    def parse(self, response):
        days = response.xpath("//div[@id='upcoming-days']/section | //div[@id='completed-days']/section")
        upcoming_days = response.xpath("//div[@id='upcoming-days']/section")
        completed_days = response.xpath("//div[@id='completed-days']/section")
        for day in days:
            date = day.xpath("h3/text()").get()
            games = day.xpath("div[1]//table")
            for game in games:
                # unique game identifier
                game_id = game.xpath("@data-game").get()

                # all game times are given in eastern time
                time = game.xpath("thead/tr[1]/th[2]/text()").get()

                if time == "FINAL":
                    completed = True
                else:
                    completed = False

                away_team = game.xpath("tbody/tr[2]/td[3]/text()").get()
                away_spread = game.xpath("tbody/tr[2]/td[4]/text()").get()
                away_chance = game.xpath("tbody/tr[2]/td[5]/text()").get()
                away_score = game.xpath("tbody/tr[2]/td[6]/text()").get(default="0")
                home_team = game.xpath("tbody/tr[3]/td[3]/text()").get()
                home_spread = game.xpath("tbody/tr[3]/td[4]/text()").get()
                home_chance = game.xpath("tbody/tr[3]/td[5]/text()").get()
                home_score = game.xpath("tbody/tr[3]/td[6]/text()").get(default="0")

                if away_spread == "PK" or home_spread == "PK":
                    away_spread = "0"
                    home_spread = "0"

                if away_spread == " ":
                    away_spread = home_spread.split("-")[-1]
                    away_spread = "+" + away_spread

                if home_spread == " ":
                    home_spread = away_spread.split("-")[-1]
                    home_spread = "+" + home_spread

                away_spread = away_spread.lstrip()
                home_spread = home_spread.lstrip()

                print(game_id)
                print(date)
                print(time)
                print(away_team)
                print(away_spread)
                print(away_chance)
                print(away_score)
                print(home_team)
                print(home_spread)
                print(home_chance)
                print(home_score)


class TeamsSpider(scrapy.Spider):
    name = 'teams'

    def start_requests(self):
        yield scrapy.Request('https://projects.fivethirtyeight.com/2019-nba-predictions/', self.parse)

    def parse(self, response):
        teams = response.xpath("/html/body/div[3]/main/div[1]/div/div[1]/table/tbody/tr")
        for team in teams:
            name = team.xpath("td[@class='team']/a/text()").get()
            full_strength_carmelo = team.xpath("td[1]/text()").get()
            current_carmelo = team.xpath("td[2]/text()").get()
            conference = team.xpath("td[@data-cell='conf']/text()").get()
            record = team.xpath("td[@class='team']/span/text()").get(default="0-0")
            record = record.split("-")
            wins = record[0]
            losses = record[1]
            proj_record = team.xpath("td[@data-cell='record']/text()").get().split("-")
            proj_wins = proj_record[0]
            proj_losses = proj_record[1]
            proj_point_diff_per_game = team.xpath("td[@data-cell='pointdiff']/text()").get()
            playoff_chance = team.xpath("td[@data-cell='make_playoffs']/text()").get()
            playoff_rating = team.xpath("td[@data-cell='playoff-rating']/span/text()").get()
            make_finals_chance = team.xpath("td[@data-cell='make_finals']/text()").get()
            win_finals_chance = team.xpath("td[@data-cell='win_finals']/text()").get()

            # if playoff_chance == u'\u2713':
            #     playoff_chance = "100%"
            # elif playoff_chance == u'\u2014':
            #     playoff_chance = "0%"

            # if playoff_rating == u'\u2014':
            #     playoff_rating = "0"

            # if make_finals_chance == u'\u2014':
            #     make_finals_chance = "0%"

            # if win_finals_chance == u'\u2014':
            #     win_finals_chance = "0%"

            print(name)
            print(full_strength_carmelo)
            print(current_carmelo)
            print(conference)
            print(wins)
            print(losses)
            print(proj_wins)
            print(proj_losses)
            print(proj_point_diff_per_game)
            print(playoff_chance)
            print(playoff_rating)
            print(make_finals_chance)
            print(win_finals_chance)


process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(GamesSpider)
process.crawl(TeamsSpider)
process.start()
