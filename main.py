import argparse
import csv
import codecs
import math
import logging
import random


def generate_schedule(array: list, loop_num: int = 1, home_away: bool = True):
    if len(array) < 2:
        return None
    elif loop_num < 1:
        logging.exception("loop_num should not be less than 1")
        return None
    elif len(array) == 2:
        game_schedule = []
        round_num = 1
        while round_num <= loop_num:
            if round_num % 2 == 0 or home_away is False:
                game_schedule.append((round_num, [(array[0], array[1])]))
            else:
                game_schedule.append((round_num, [(array[1], array[0])]))
            round_num += 1

        return game_schedule

    if len(array) % 2 != 0:
        array.append('Empty Team')

    total_num = len(array)
    one_round_num = math.ceil(total_num / 2) * 2 - 1
    left_team = array[0:math.ceil(total_num / 2)]
    right_team = array[math.ceil(total_num / 2):]
    game_schedule = []
    round_num = 1
    while round_num <= one_round_num:
        signal = random.randint(0, 9)  # decide the home and away
        if signal % 2 == 0:
            detail_schedule = list(zip(left_team, right_team))
        else:
            detail_schedule = list(zip(right_team, left_team))

        game_schedule.append((round_num, detail_schedule))
        tmp1 = left_team[1]
        tmp2 = right_team[-1]
        for i in range(2, len(left_team)):
            left_team[i - 1] = left_team[i]
        for i in range((len(left_team) - 1), 0, -1):
            right_team[i] = right_team[i - 1]
        right_team[0] = tmp1
        left_team[-1] = tmp2
        round_num += 1

    if loop_num >= 1:
        while round_num <= one_round_num * loop_num:
            refer_schedule = game_schedule[(round_num - 1) % one_round_num][1]
            detail_schedule = []
            for detail_game in refer_schedule:
                team1, team2 = detail_game
                if home_away is True and math.ceil(round_num / one_round_num) % 2 == 0:
                    detail_schedule.append((team2, team1))
                else:
                    detail_schedule.append((team1, team2))
            game_schedule.append((round_num, detail_schedule))
            round_num += 1

    return game_schedule


def output_schedule(schedule_arr: list, output_mode: str = "csv", output_path: str = "schedule.csv"):
    if output_mode == "print":
        for round_game in schedule_arr:
            print(f"Round {round_game[0]}:")
            for detail_game in round_game[1]:
                if detail_game[0] == "Empty Team" or detail_game[1] == "Empty Team":
                    continue
                print(f"{detail_game[0]} vs {detail_game[1]}")
    elif output_mode == "csv":
        with open(output_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["Round", "Home Team", "Away Team"])
            for round_game in schedule_arr:
                round_num = round_game[0]
                for detail_game in round_game[1]:
                    if detail_game[0] == "Empty Team" or detail_game[1] == "Empty Team":
                        continue
                    writer.writerow([round_num, detail_game[0], detail_game[1]])
    else:
        logging.exception("Illegal output mode")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="The single tournament schedule tool")
    parser.add_argument("--loop_num", type=int, default=1, help="The num of the loop")
    parser.add_argument("--home_away", type=bool, default=True, help="Set whether schedule needs home away mode")
    parser.add_argument("--input", type=str, default="team_list.txt",
                        help="The location where the team list file stores")
    parser.add_argument("--output_mode", type=str, default="csv",
                        help="The location where the team list file stores")
    parser.add_argument("--output", type=str, default="schedule.csv",
                        help="The output path that the generated schedule stores, if output mode is 'csv',"
                             "and this argument is invalid")
    args = parser.parse_args()

    loop_num = args.loop_num
    home_away = args.home_away
    in_path = args.input
    out_path = args.output
    out_mode = args.output_mode

    with open(in_path, "r", encoding="utf-8-sig") as team_file:
        team_list = team_file.readlines()
        for i in range(len(team_list)):
            team_list[i] = team_list[i].strip("\n")
        schedule = generate_schedule(team_list, loop_num, home_away)
        output_schedule(schedule, out_mode, out_path)
