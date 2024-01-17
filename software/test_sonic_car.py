from sonic_car import *

def main():
    sc = SonicCar()
    sc.make_measures() # 100 Mal

    distance_obs = sc.get_distance_to_obstacle() # 1 Mal
    print(f'distance: {distance_obs}')
    


if __name__ == '__main__':
    main()
