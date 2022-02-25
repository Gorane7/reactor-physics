from particle import Particle
from value import Value

particle_data = {
    "0n1": (8071, "neutron"),
    "1H1": (7289, "hydrogen"),
    "1H2": (13135.7, "deuterium"),
    "1H3": (14949.8, "tritium"),
    "2He3": (14931.2, "helium-3"),
    "2He4": (2424.9, "helium-4"),
    "92U235": (40918.8, "uranium-235")
}

c = Value(3*10**8, "m/s")


particles = {key: Particle(key, *data) for key, data in particle_data.items()}
