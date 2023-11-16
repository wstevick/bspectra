#!/usr/bin/python3
import collections

bin_size = 0.25
max_energy = 2000

visible_x_rays = [
    (r"$L_2M_1 L_\eta$", 10.3082),
    (r"$L_1M_1$", 10.9287),
    (r"$L_2M_3 L_{\beta 17}$", 10.99),
    (r"$L_1M_2 L_{\beta 4}$", 11.2048),
    (r"$L_3N_1 L_{\beta 6}$", 11.1564),
    (r"$L_2M_4 L_{\beta 1}$", 11.442),
    (r"$L_3N_2$", 11.2755),
    (r"$L_3N_3$", 11.371),
    (r"$L_1M_3 L_{\beta 3}$", 11.6105),
    (r"$L_2M_5$", 11.5272),
    (r"$L_3N_4 L_{\beta 15}$", 11.564),
    (r"$L_3N_5 L_{\beta 2}$", 11.58212),
    (r"$L_3N_6 L_{u (\prime)}$", 11.8287),
    (r"$L_3N_7 L_u$", 11.8323),
    # (r"L3 edge", 11.92778),
    (r"$L_2N_2$", 13.0894),
    (r"$L_2N_3$", 13.18489),
    (r"$L_2N_4 L_{\gamma 1}$", 13.3779),
    (r"$L_2N_5$", 13.39601),
    (r"$L_1N_1$", 13.5908),
    (r"$L_1N_2 L_{\gamma 2}$", 13.71),
    (r"$L_2N_6 L_v$", 13.6425),
    (r"$L_2N_7$", 13.6462),
    # (r"L2 edge", 13.74167),
]

groups = collections.defaultdict(list)

for name, energy in visible_x_rays:
    bin_id = int((max_energy - energy) / bin_size)
    groups[bin_id].append(name)

for conflicts in groups.values():
    if len(conflicts) > 1:
        print(*conflicts, sep=", ")
