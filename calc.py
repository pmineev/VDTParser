def filter_leaderboards(leaderboards, nickname):
    return list(
        filter(
            lambda l:
            any(
                map(
                    lambda f:
                    f.player == nickname,
                    l.flights
                )
            ),
            leaderboards
        )
    )


def get_abs_vdt_deltas(leaderboards, nickname):
    deltas = dict()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas[leaderboard.date] = flight.delta

    return deltas


def get_abs_world_deltas(leaderboards, nickname):
    deltas = dict()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas[leaderboard.date] = flight.time - leaderboard.world_record

    return deltas


def get_rel_vdt_deltas(leaderboards, nickname):
    deltas = dict()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas[leaderboard.date] = flight.delta / leaderboard.flights[0].time * 100

    return deltas


def get_rel_world_deltas(leaderboards, nickname):
    deltas = dict()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas[leaderboard.date] = (flight.time - leaderboard.world_record) / leaderboard.world_record * 100

    return deltas
