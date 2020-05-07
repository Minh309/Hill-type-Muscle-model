import H_muscle
import numpy as np

def main():
	#We consider three different values of total muscle-tendon length
	l_mts = np.array([0.30, 0.31, 0.32])
	#Call the Hill_type_muscle class
	Hill_Muscle = H_muscle.Hill_type_muscle()
	#Create a muscle excitation profile
	u = np.linspace(0,1,200)
	for l_mt in l_mts:
		#Show the value of active muscle force function
		Hill_Muscle.mes_active_muscle_force_value(l_mt)
		#Show the value of passive muscle force function
		Hill_Muscle.mes_passive_muscle_force_value(l_mt)
		#Calculate the active muscle force 
		F_A = Hill_Muscle.cal_active_muscle_force(l_mt, u)
		#Calculate the total muscle force
		F = Hill_Muscle.cal_muscle_fiber_force(l_mt,u)
		#Set the title for the line graph
		title = 'Total muscle-tendon length = ' + f'{l_mt}' + ' m'
		#Plot the result 
		Hill_Muscle.plot_force(u, F_A, F, title)

if __name__ == '__main__':
        main() 