
import numpy as np
import matplotlib.pyplot as plt
import math

# generation of routes of cars
def generate_routes_train(seed, MAX_STEPS):
    #np.random.seed(seed)  # make tests reproducible

    n_main_cars_generated = 22000 #main veh (应该是总数，考虑3个小时的仿真)
    n_ramp_cars_generated = 8000 #ramp veh
    M_OR_R = n_main_cars_generated/(n_main_cars_generated+n_ramp_cars_generated); #阈值

    # the generation of cars is distributed according to a weibull distribution
    #main_timings = np.random.weibull(2, n_main_cars_generated)
    main_timings = np.random.uniform(0,5400,22000)
    main_timings = np.sort(main_timings) #把分布排序（从小到大）
    print("========start main=============")
    print(len(main_timings))
    print("==========end main=============")
    
    #ramp_timings = np.random.weibull(2, n_ramp_cars_generated)
    ramp_timings = np.random.uniform(0,5400,8000)
    ramp_timings = np.sort(ramp_timings) #把分布排序（从小到大）
    print("========start ramp=============")
    print(len(ramp_timings))
    print("==========end ramp=============")
    #for test
    '''
    print("weibull length: ",len(timings))
    print(timings)
    plt.hist(timings, bins = 64)
    '''

    # reshape the distribution to fit the interval 0:MAX_STEPS
    main_car_gen_steps = [] #计算每一步的主线车流量
    #main_car_gen_steps = list() #计算每一步的主线车流量
    ramp_car_gen_steps = []#计算每一步的匝道车流量
    min_old = math.floor(main_timings[1])#timings第一个元素
    max_old = math.ceil(main_timings[-1])#timings最后一个元素
    min_new = 0
    max_new = MAX_STEPS
    for value in main_timings:
        main_car_gen_steps = np.append(main_car_gen_steps, ((max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)

    #四舍五入取整
    main_car_gen_steps = np.rint(main_car_gen_steps).tolist() # round every value to int -> effective steps when a car will be generated
    #========================================================
    min_old = math.floor(ramp_timings[1])#timings第一个元素
    max_old = math.ceil(ramp_timings[-1])#timings最后一个元素
 
    for value in ramp_timings:
        ramp_car_gen_steps = np.append(ramp_car_gen_steps, ((max_new - min_new) / (max_old - min_old)) * (value - max_old) + max_new)

    #四舍五入取整
    ramp_car_gen_steps = np.rint(ramp_car_gen_steps).tolist() # round every value to int -> effective steps when a car will be generated
    #========================================================
    #for test 2
    np.set_printoptions(threshold=np.inf)
    print("ramp car steps length: ",len(ramp_car_gen_steps))
    print(ramp_car_gen_steps)
    plt.hist(ramp_car_gen_steps, bins = 180) #bins是柱状图的数目
    #plt.hist(car_gen_steps, bins = len(car_gen_steps))

    # produce the file for cars generation, one car per line
    with open("freewayNetwork/new8.rou.xml", "w") as routes:
        print("""<routes>
        <vType accel="1.0" decel="4.5" id="standard_car" length="5.0" minGap="2.5" maxSpeed="34" sigma="0.5" /> 

        <route id="route_0" edges="320972144 320972153 320972153.207 232373755 232373755.215 232373755.451 320972162 320972160 509503616#0"/>
        <route id="route_1" edges="320972144 320972153 320972153.207 7341726 320972173 320972175"/>
        <route id="route_2" edges="320972174#0 320972169 320972169.434 320972162 320972160 509503616#0"/>""", file=routes)#file = routes：要写入的文件对象。routes在此处是指针。
        
        #maxSpeed="34":34m/s = 122km/h
        #原来的路径
        #<route id="route_0" edges="320972144 320972153 232373755 320972162 320972160 509503616#0"/>
        #<route id="route_1" edges="320972144 320972153 7341726 320972173 320972175"/>
        #<route id="route_2" edges="320972174#0 320972169 320972169.434 320972162 320972160 509503616#0"/>""", file=routes)#file = routes：要写入的文件对象。routes在此处是指针。
        car_counter = 0;
        for step in range(0, MAX_STEPS):
            if step in main_car_gen_steps:
                for i in range(0, main_car_gen_steps.count(step)):
                    straight_or_turn = np.random.uniform() #是否从匝道下去
                    if straight_or_turn < 0.8:  # choose direction: straight
                        print('        <vehicle id="route_0_%i" type="standard_car" route="route_0" depart="%s"  departLane="random" departSpeed="5" />' % (car_counter, step), file=routes)
                        car_counter+=1;
                    else: #go off-ramp
                        print('        <vehicle id="route_1_%i" type="standard_car" route="route_1" depart="%s"  departLane="random" departSpeed="5" />' % (car_counter, step), file=routes)
                        car_counter+=1;
                
            if step in ramp_car_gen_steps:
                for j in range(0, ramp_car_gen_steps.count(step)):
                    print('        <vehicle id="route_2_%i" type="standard_car" route="route_2" depart="%s"  departLane="random" departSpeed="10" />' % (car_counter, step), file=routes)
                    car_counter+=1;
        
        print("</routes>", file=routes)

        #return traffic_code
    
if __name__ == "__main__":
    generate_routes_train(1, 5400)#seed = 10, max step = 10800 (3h×3600=10800)
    