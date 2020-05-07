import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt

# Define the Hill-type muscle class:
class Hill_type_muscle():
    def __init__(self,
                F_0 = 3549,  #Muscle maximal isometric force = 3549 N
                l_0 = 0.05,  #Muscle optimal fibre length = 0.05m
                l_t = 0.25,  #Tendon infinitely stiff with a constant length = 0.25m
                phi_0 = 0.2, #Pennation angle = 0.20 rad
                A = -0.1):   #Shape factor A = -0.1
        
        self.F_0 = F_0
        self.l_0 = l_0
        self.l_t = l_t
        self.phi_0 = phi_0
        self.A = A
    
    ###########################################################################################
    # Name: cal_muscle_activation                                                             # 
    # Input: Muscle excitation value (u)                                                      #
    # Output: Muscle activation value (a)                                                     #
    # This method returns the muscle activation from muscle excitation profile                #
    ###########################################################################################
    
    def cal_muscle_activation(self, u):
        a = (np.exp(self.A*u) - 1)/(np.exp(self.A) - 1)
        return a
    
    ######################################################################################################
    # Name: cal_muscle_fiber_length                                                                      # 
    # Input: Total muscle-tendon length (l_mt)                                                           #
    # Output: Muscle fiber length (l_m)                                                                  #
    # This method returns the muscle fiber length from the total muscle-tendon length                    #
    ######################################################################################################
    
    def cal_muscle_fiber_length(self, l_mt):
        l_m = np.sqrt((self.l_0*np.sin(self.phi_0))**2 + (l_mt - self.l_t)**2)
        return l_m
    
    #################################################################################################################
    # Name: cal_normalized_muscle_fiber_length                                                                      #
    # Input: Total muscle-tendon length (l_mt)                                                                      #
    # Output: Normalised Muscle fiber length (l_hat)                                                                #
    # This method returns the normalised muscle fiber length from the total muscle-tendon length                    #
    #################################################################################################################

    def cal_normalized_muscle_fiber_length(self, l_mt):
        l_m = self.cal_muscle_fiber_length(l_mt)
        l_hat = l_m/self.l_0
        return l_hat
    
    ######################################################
    # Name: get_active_force_length_function             #
    # Input: None                                        #
    # Output: Active force-length function (f_a)         #
    # This method returns the active force-length curve  #
    ######################################################

    def get_active_force_length_function(self):
        x = np.array([-5, 0, 0.401, 0.402, 0.4035, 0.52725, 0.62875, 0.71875, 0.86125, 1.045, 1.2175, 1.43875, 1.61875, 1.62, 1.621, 2.2, 5])
        y = np.array([0, 0, 0, 0, 0, 0.226667, 0.636667, 0.856667, 0.95, 0.993333, 0.77, 0.246667, 0, 0, 0, 0, 0])
        f_a = interpolate.interp1d(x, y, kind = 'cubic')
        return f_a

    ######################################################
    # Name: get_passive_force_length_function            #
    # Input: None                                        #
    # Output: Passive force-length function (f_p)        #
    # This method returns the passive force-length curve #
    ######################################################
   
    def get_passive_force_length_function(self):
        x = np.array([-5, 0.998, 0.999, 1, 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.601, 1.602, 5])
        y = np.array([0, 0, 0, 0, 0.035, 0.12, 0.26, 0.55, 1.17, 2, 2, 2, 2])
        f_p = interpolate.interp1d(x, y, kind = 'cubic')
        return f_p

    ################################################################################################################
    # Name: get_active_force_length_value                                                                          #
    # Input: Total muscle-tendon length (l_mt)                                                                     #
    # Output: Active force-length value corresponding to one specific value of muscle fiber length (f_am)          #
    # This method returns the active force-length value corresponding to the specific value of muscle fiber length #
    ################################################################################################################

    def get_active_force_length_value(self, l_mt):
        f_a = self.get_active_force_length_function()
        l_hat = self.cal_normalized_muscle_fiber_length(l_mt)
        f_am = f_a(l_hat)
        return f_am
        
    #################################################################################################################
    # Name: get_passive_force_length_value                                                                          #
    # Input: Total muscle-tendon length (l_mt)                                                                      #
    # Output: Passive force-length value corresponding to one specific value of muscle fiber length (f_pm)          #
    # This method returns the passive force-length value corresponding to the specific value of muscle fiber length #
    #################################################################################################################
        
    def get_passive_force_length_value(self, l_mt):
        f_p = self.get_passive_force_length_function()
        l_hat = self.cal_normalized_muscle_fiber_length(l_mt)
        f_pm = f_p(l_hat)
        return f_pm

    ################################################################################################################
    # Name: mes_active_muscle_force_value                                                                          #
    # Input: Total muscle-tendon length (l_mt)                                                                     #
    # Output: A message                                                                                            #
    # This method prints a message showing the active force-length value corresponding to the value of l_mt        #
    ################################################################################################################

    def mes_active_muscle_force_value(self, l_mt):
        f_am = self.get_active_force_length_value(l_mt)
        message = 'Active Force-Length Value when l_mt = ' + f'{l_mt}' + 'm is ' + f'{np.round(f_am,4)}'
        print(message)

    #################################################################################################################
    # Name: mes_passive_muscle_force_value                                                                          #
    # Input: Total muscle-tendon length (l_mt)                                                                      #
    # Output: A message                                                                                             #
    # This method prints a message showing the passive force-length value corresponding to the value of l_mt        #
    #################################################################################################################

    def mes_passive_muscle_force_value(self, l_mt):
        f_pm = self.get_passive_force_length_value(l_mt)
        message = 'Passive Force-Length Value when l_mt = ' + f'{l_mt}' + 'm is ' + f'{np.round(f_pm,4)}'
        print(message)
    
    #######################################################################################################
    # Name: cal_active_muscle_force                                                                       #
    # Input: Total muscle-tendon length (l_mt), muscle excitation value (u)                               #
    # Output: Active muscle force (F_A)                                                                   #
    # This method returns the active muscle force generated by the contractile element                    #
    #######################################################################################################

    def cal_active_muscle_force(self, l_mt, u):
        a = self.cal_muscle_activation(u)
        f_am = self.get_active_force_length_value(l_mt)
        F_A = f_am*self.F_0*a
        return F_A
    
    ####################################################################################################
    # Name: cal_passive_muscle_force                                                                   #
    # Input: Total muscle-tendon length (l_mt)                                                         #
    # Output: Passive muscle force (F_P)                                                               #
    # This method returns the passive muscle force generated by the passive element                    #
    ####################################################################################################

    def cal_passive_muscle_force(self, l_mt):
        f_pm = self.get_passive_force_length_value(l_mt)
        F_P = f_pm*self.F_0
        return F_P

    #########################################################################
    # Name: cal_muscle_fiber_force                                          #
    # Input: Total muscle-tendon length (l_mt), muscle excitation value (u) #
    # Output: total muscle fiber force (F_P)                                #
    # This method returns the total muscle force                            #
    #########################################################################

    def cal_muscle_fiber_force(self, l_mt, u):
        a = self.cal_muscle_activation(u)
        F_A = self.cal_active_muscle_force(l_mt, a)
        F_P = self.cal_passive_muscle_force(l_mt)
        F = F_A + F_P
        return F
    
    ##################################################################################################################
    # Name: plot_force                                                                                               #
    # Input: muscle excitation value (u), active muscle force (F_A), total muscle force (F), title of the graph      #
    # Output: a line graph                                                                                           #
    # This method plots the calculated active muscle force and total muscle force over a range of muscle excitations #
    ##################################################################################################################

    def plot_force(self, u, active_force, total_force, title):
        legends = ['Active Force', 'Total Force']
        y_label = 'Muscle Force [N]'
        x_label = 'Muscle Excitation'
        fig, ax = plt.subplots()
        ax.tick_params(axis='both', which='major', labelsize=15)
        ax.set_ylim(0,3600)
        ax.set_xlim(0,1)
        ax.yaxis.get_major_ticks()[0].label1.set_visible(False)         #Hide the first tick
        ax.plot(u, active_force, 'r', linewidth=4)
        ax.plot(u, total_force, 'g', linewidth =4)
        ax.set_ylabel(y_label,fontsize=20)
        ax.set_xlabel(x_label,fontsize=20)
        ax.set_title(title,fontsize=20)
        ax.legend(legends, loc = 'lower right',fontsize=20)
        fig.set_size_inches(13,7)
        plt.tight_layout()
        plt.grid()
        plt.show()