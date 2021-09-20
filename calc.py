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
    deltas = list()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas.append(flight.delta)

    return deltas


def get_abs_world_deltas(leaderboards, nickname):
    deltas = list()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas.append(flight.time - leaderboard.world_record)

    return deltas


def get_rel_vdt_deltas(leaderboards, nickname):
    deltas = list()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas.append(flight.delta / leaderboard.flights[0].time * 100)

    return deltas


def get_rel_world_deltas(leaderboards, nickname):
    deltas = list()
    for leaderboard in leaderboards:
        flight = [f for f in leaderboard.flights if f.player == nickname][0]
        deltas.append((flight.time - leaderboard.world_record) / leaderboard.world_record * 100)

    return deltas


def get_deltas(leaderboards, nickname):
    filtered_leaderboards = filter_leaderboards(leaderboards, nickname)
    dates = [lb.date for lb in filtered_leaderboards]
    deltas = {
        'dates': dates,
        'abs_vdt': get_abs_vdt_deltas(filtered_leaderboards, nickname),
        'abs_world': get_abs_world_deltas(filtered_leaderboards, nickname),
        'rel_vdt': get_rel_vdt_deltas(filtered_leaderboards, nickname),
        'rel_world': get_rel_world_deltas(filtered_leaderboards, nickname),
    }

    return deltas
